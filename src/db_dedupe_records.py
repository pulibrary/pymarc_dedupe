from os import listdir
from os.path import isfile, join
import dedupe
import psycopg2
import psycopg2.extras
from config import settings
from src.marc_to_db import MarcToDb
from src.machine_learning_model import MachineLearningModel
from src.readable import Readable

RECORD_SELECT = """SELECT
                    id, title, author, publication_year, pagination, edition, publisher_name, type_of, is_electronic_resource
                    FROM records;
                """


class DbDedupeRecords(MachineLearningModel):
    def __init__(self, input_directory, output_directory, match_threshold=0.5):
        super().__init__(output_directory, match_threshold)
        for path in listdir(input_directory):
            full_path = join(input_directory, path)
            if isfile(full_path):
                # save to database
                MarcToDb(full_path).to_db()
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

    def deduper(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print("reading from", self.settings_file_path)
                model = dedupe.StaticDedupe(sf)
        except FileNotFoundError:
            model = dedupe.Dedupe(self.fields())
            model = self.train_and_write_model(model)

        return model

    def prepare_training(self, model):
        with self.read_con.cursor("donor_select") as cur:
            cur.execute(RECORD_SELECT)
            # temp_d = {i: row for i, row in enumerate(cur)}
            temp_d = dict(enumerate(cur))
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                return model.prepare_training(temp_d, training_file=tf)
        except FileNotFoundError:
            return model.prepare_training(temp_d)

        del temp_d

    def train_and_write_model(self, model):
        self.prepare_training(model)
        self.console_label(model)
        model.train()
        # When finished, save our training away to disk
        self.write_training(model)
        self.write_settings(model)
        # Remove memory intensive objects used for training
        model.cleanup_training()
        return model

    def block(self, model):
        print("blocking...")
        print("creating blocking_map table")
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS blocking_map")
                cur.execute("CREATE TABLE blocking_map (block_key text, id TEXT)")
        print("creating inverted index")
        for field in model.fingerprinter.index_fields:
            with self.read_con.cursor("field_values") as cur:
                cur.execute(f"SELECT DISTINCT {field} FROM records")
                field_data = (row[field] for row in cur)
                model.fingerprinter.index(field_data, field)

        print("writing blocking map")
        with self.read_con.cursor("donor_select") as read_cur:
            read_cur.execute(RECORD_SELECT)

            full_data = ((row["id"], row) for row in read_cur)
            b_data = model.fingerprinter(full_data)

            with self.write_con:
                with self.write_con.cursor() as write_cur:
                    write_cur.copy_expert(
                        "COPY blocking_map FROM STDIN WITH CSV",
                        Readable(b_data),
                        size=10000,
                    )

        model.fingerprinter.reset_indices()
        print("indexing block_key")
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

                print("creating entity_map database")
                cur.execute(
                    "CREATE TABLE entity_map "
                    "(id TEXT, canon_id TEXT, "
                    " cluster_score FLOAT, PRIMARY KEY(id))"
                )
        with open("pairs.sql", "r", encoding="utf-8") as file:
            pairs_sql = file.read()
        with self.read_con.cursor(
            "pairs", cursor_factory=psycopg2.extensions.cursor
        ) as read_cur:
            read_cur.execute(pairs_sql)
            print("clustering...")
            clustered_dupes = model.cluster(
                model.score(self.record_pairs(read_cur)), threshold=self.match_threshold
            )
            print("writing results")
            with self.write_con:
                with self.write_con.cursor() as write_cur:
                    write_cur.copy_expert(
                        "COPY entity_map FROM STDIN WITH CSV",
                        Readable(cluster_ids(clustered_dupes)),
                        size=10000,
                    )
        with self.write_con:
            with self.write_con.cursor() as cur:
                cur.execute("CREATE INDEX head_index ON entity_map (canon_id)")

    def record_pairs(self, result_set):
        for i, row in enumerate(result_set):
            a_record_id, a_record, b_record_id, b_record = row
            record_a = (a_record_id, a_record)
            record_b = (b_record_id, b_record)

            yield record_a, record_b

            if i % 10000 == 0:
                print(i)


def cluster_ids(clustered_dupes):
    for cluster, scores in clustered_dupes:
        cluster_id = cluster[0]
        for donor_id, score in zip(cluster, scores):
            yield donor_id, cluster_id, score
