import os.path
import csv
import dedupe
from src.link_records_file import LinkRecordsFile


class DedupeRecords:
    def __init__(self, input_file, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        linked_records_file = LinkRecordsFile(input_file, True)
        self.input_file = linked_records_file.csv_path
        self.data_d = linked_records_file.read_data()
        self.output_file_path = os.path.join(
            output_directory, "data_matching_output.csv"
        )
        self.settings_file_path = os.path.join(
            output_directory, "data_matching_learned_settings"
        )
        self.training_file_path = os.path.join(
            output_directory, "data_matching_training.json"
        )

    def fields(self):
        return [
            dedupe.variables.String("title"),
            dedupe.variables.String("author", has_missing=True),
            dedupe.variables.String("publication_year"),
            dedupe.variables.String("pagination", has_missing=True),
            dedupe.variables.Exists("edition"),
            dedupe.variables.String("edition", has_missing=True),
            dedupe.variables.String("publisher_name", has_missing=True),
            dedupe.variables.Exact("type_of"),
            dedupe.variables.Exact("is_electronic_resource"),
        ]

        # This method really needs to be broken up

    def deduper(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print("reading from", self.settings_file_path)
                deduper = dedupe.StaticDedupe(sf)
        except FileNotFoundError:
            deduper = dedupe.Dedupe(self.fields())
            self.prepare_training(deduper)
            self.console_label(deduper)
            deduper.train()
            # When finished, save our training away to disk
            self.write_training(deduper)
            self.write_settings(deduper)

        return deduper

    def prepare_training(self, deduper):
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                return deduper.prepare_training(
                    self.data_d, training_file=tf, sample_size=1500
                )
        except FileNotFoundError:
            return deduper.prepare_training(self.data_d, sample_size=1500)

    def console_label(self, deduper):
        print("starting active labeling...")
        dedupe.console_label(deduper)

    def cluster(self, deduper):
        print("clustering...")
        clustered_dupes = deduper.partition(self.data_d, 0.5)
        print("# duplicate sets", len(clustered_dupes))

        cluster_membership = {}
        for cluster_id, (records, scores) in enumerate(clustered_dupes):
            for record_id, score in zip(records, scores):
                cluster_membership[record_id] = {
                    "Cluster ID": cluster_id,
                    "Link Score": score,
                }
        self.write_output(cluster_membership)

    def write_training(self, linker):
        with open(self.training_file_path, "w", encoding="utf-8") as tf:
            linker.write_training(tf)

    def write_settings(self, linker):
        with open(self.settings_file_path, "wb") as sf:
            linker.write_settings(sf)

    def write_output(self, cluster_membership):
        print("Writing duplicates to output file path: " + self.output_file_path)
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            header_unwritten = True

            for _filename in enumerate((self.input_file)):
                with open(self.input_file, encoding="utf-8") as f_input:
                    reader = csv.DictReader(f_input)

                    if header_unwritten:
                        fieldnames = [
                            "Cluster ID",
                            "Link Score",
                        ] + reader.fieldnames

                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()

                        header_unwritten = False

                    for row_id, row in enumerate(reader):
                        record_id = row_id
                        cluster_details = cluster_membership.get(record_id, {})
                        row.update(cluster_details)

                        writer.writerow(row)
