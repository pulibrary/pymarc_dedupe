import threading
from os import listdir
from os.path import isfile, join
import time
import dedupe
import psycopg2
import psycopg2.extras
from config import settings
from src.ingest.marc_to_db import MarcToDb
from src.models.machine_learning_model import MachineLearningModel
from src.readable import Readable

RECORD_SELECT = """SELECT
                    id, title, author, publication_year, pagination, edition, publisher_name, type_of, is_electronic_resource
                    FROM records;
                """


class DbDedupeRecords(MachineLearningModel):
    def __init__(self, input_directory, output_directory, match_threshold=0.5):
        MarcToDb.find_or_create_table()
        super().__init__(output_directory, match_threshold)
        directory_list = listdir(input_directory)
        if len(directory_list) == 0:
            raise ValueError(f"Input directory {input_directory} must include files")
        threads = []
        for path in directory_list:
            full_path = join(input_directory, path)
            if isfile(full_path):
                t = threading.Thread(target=ingest_to_db, args=(full_path,))
                threads.append(t)
        self.read_con = psycopg2.connect(
            database=settings.db_name,
            user=settings.db_user,
            host=settings.db_host,
            port=settings.db_port,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        self.write_con = psycopg2.connect(
            database=settings.db_name,
            user=settings.db_user,
            host=settings.db_host,
            port=settings.db_port,
        )
        for t in threads:
            t.start()

        for t in threads:
            t.join()

    # pylint: disable=duplicate-code
    def deduper(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print(
                    f"""time: {time.asctime(time.localtime())} -
                        reading from {self.settings_file_path}"""
                )
                model = dedupe.StaticDedupe(sf)
        except FileNotFoundError:
            model = dedupe.Dedupe(self.fields())
            model = self.train_and_write_model(model)

        return model

    # pylint: enable=duplicate-code

    def prepare_training(self, model):
        with self.read_con.cursor("record_select") as cur:
            print("Building temporary dictionary of records for training")
            cur.execute(RECORD_SELECT)
            temp_d = dict(enumerate(cur))
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                print(
                    f"""time: {time.asctime(time.localtime())} -
                    Loading training data from {self.training_file_path}
                     - you can skip console label if you would like"""
                )
                our_model = model.prepare_training(temp_d, training_file=tf)
                print(f"time: {time.asctime(time.localtime())} - training file loaded")
        except FileNotFoundError:
            print(
                f"time: {time.asctime(time.localtime())} - "
                "No training file found, preparing training"
            )
            our_model = model.prepare_training(temp_d)

        print(f"time: {time.asctime(time.localtime())} - deleting temp dictionary")
        del temp_d

        return our_model

    def train_and_write_model(self, model):
        print(f"time: {time.asctime(time.localtime())} - about to prepare training")
        self.prepare_training(model)
        print(f"time: {time.asctime(time.localtime())} - about to console label")
        self.console_label(model)
        model.train()
        # When finished, save our training away to disk
        self.write_training(model)
        self.write_settings(model)
        # Remove memory intensive objects used for training
        model.cleanup_training()
        return model

    def block(self, model):
        print(f"time: {time.asctime(time.localtime())} - blocking...")
        print(f"time: {time.asctime(time.localtime())} - creating blocking_map table")
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS blocking_map")
                cur.execute("CREATE TABLE blocking_map (block_key text, id TEXT)")
        print(f"time: {time.asctime(time.localtime())} - creating inverted index")
        for field in model.fingerprinter.index_fields:
            with self.read_con.cursor("field_values") as cur:
                cur.execute(f"SELECT DISTINCT {field} FROM records")
                field_data = (row[field] for row in cur)
                model.fingerprinter.index(field_data, field)

        print(f"time: {time.asctime(time.localtime())} - writing blocking map")
        with self.read_con.cursor("record_select") as read_cur:
            read_cur.execute(RECORD_SELECT)

            full_data = ((row["id"], row) for row in read_cur)
            b_data = model.fingerprinter(full_data)

            with self.write_con:
                with self.write_con.cursor() as write_cur:
                    write_cur.copy_expert(
                        "COPY blocking_map FROM STDIN WITH CSV",
                        Readable(b_data),
                        size=25000,
                    )

        model.fingerprinter.reset_indices()
        print(f"time: {time.asctime(time.localtime())} - indexing block_key")
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute(
                    "CREATE UNIQUE INDEX ON blocking_map "
                    "(block_key text_pattern_ops, id)"
                )

    def cluster(self, model):
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS entity_map")

                print(
                    f"time: {time.asctime(time.localtime())} - creating entity_map table"
                )
                cur.execute(
                    "CREATE TABLE entity_map "
                    "(id TEXT, cluster_id TEXT, "
                    " cluster_score FLOAT, PRIMARY KEY(id))"
                )
        with open("pairs.sql", "r", encoding="utf-8") as file:
            pairs_sql = file.read()
        with self.read_con.cursor(
            "pairs", cursor_factory=psycopg2.extensions.cursor
        ) as read_cur:
            read_cur.execute(pairs_sql)
            print(f"time: {time.asctime(time.localtime())} - clustering...")
            clustered_dupes = model.cluster(
                model.score(self.record_pairs(read_cur)), threshold=self.match_threshold
            )
            print(
                f"time: {time.asctime(time.localtime())} - writing results to database"
            )
            # this is very slow on large data sets and only across two CPUs
            # Is there a way to multi-thread here?
            # Also using a ton of swap memory
            # Does not seem to be writing to database in chunks?
            # Even though I think it's writing to stdin in chunks?
            with self.write_con:
                with self.write_con.cursor() as write_cur:
                    write_cur.copy_expert(
                        "COPY entity_map FROM STDIN WITH CSV",
                        Readable(cluster_ids(clustered_dupes)),
                        size=10000,
                    )
        print(f"time: {time.asctime(time.localtime())} - adding index to entity_map")
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute("CREATE INDEX head_index ON entity_map (cluster_id)")

    def record_pairs(self, result_set):
        for i, row in enumerate(result_set):
            a_record_id, a_record, b_record_id, b_record = row
            record_a = (a_record_id, a_record)
            record_b = (b_record_id, b_record)

            yield record_a, record_b

            if i % 10000 == 0:
                print(i)

    def create_table_for_csv(self):
        print(
            f"time: {time.asctime(time.localtime())} - creating table for output to csv"
        )
        with self.read_con.cursor() as cur:
            cur.execute("""CREATE TEMPORARY TABLE for_csv
                        AS SELECT cluster_id, entity_map.id, cluster_score, title, publication_year, pagination, edition, publisher_name, type_of, is_electronic_resource, source_file, goldrush
                        FROM entity_map 
                        INNER JOIN records 
                        ON entity_map.id = records.id 
                        ORDER BY cluster_id, cluster_score;
""")

    def write_to_csv(self):
        print(f"time: {time.asctime(time.localtime())} - writing results to csv")
        with self.read_con.cursor() as cur:
            with open(self.output_file_path, "w", encoding="utf-8") as file:
                cur.copy_expert("COPY for_csv TO STDOUT WITH CSV HEADER", file)


def cluster_ids(clustered_dupes):
    for cluster, scores in clustered_dupes:
        cluster_id = cluster[0]
        for record_id, score in zip(cluster, scores):
            yield record_id, cluster_id, score


def ingest_to_db(full_path):
    MarcToDb(full_path).to_db()
