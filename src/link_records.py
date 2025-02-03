import os.path
import csv
import dedupe
from src.link_records_file import LinkRecordsFile


class LinkRecords:
    def __init__(self, left_file, right_file, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self.left_file = LinkRecordsFile(left_file).csv_path
        self.right_file = LinkRecordsFile(right_file).csv_path
        self.left_data = LinkRecordsFile(left_file).read_data()
        self.right_data = LinkRecordsFile(right_file).read_data()
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

    def linker(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print("reading from", self.settings_file_path)
                linker = dedupe.StaticRecordLink(sf)
        except FileNotFoundError:
            linker = dedupe.RecordLink(self.fields())
            self.prepare_training(linker)
            self.console_label(linker)
            linker.train()
            # When finished, save our training away to disk
            self.write_training(linker)
            self.write_settings(linker)

        return linker

    def prepare_training(self, linker):
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                return linker.prepare_training(
                    self.left_data, self.right_data, training_file=tf, sample_size=1500
                )
        except FileNotFoundError:
            return linker.prepare_training(
                self.left_data, self.right_data, sample_size=1500
            )

    def console_label(self, linker):
        print("starting active labeling...")
        dedupe.console_label(linker)

    def cluster(self, linker):
        print("clustering...")
        linked_records = linker.join(
            self.left_data, self.right_data, 0.3, "many-to-many"
        )
        print("# duplicate sets", len(linked_records))

        cluster_membership = {}
        for cluster_id, (cluster, score) in enumerate(linked_records):
            for record_id in cluster:
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

            for fileno, filename in enumerate((self.left_file, self.right_file)):
                with open(filename, encoding="utf-8") as f_input:
                    reader = csv.DictReader(f_input)

                    if header_unwritten:
                        fieldnames = [
                            "Cluster ID",
                            "Link Score",
                            "source file",
                        ] + reader.fieldnames

                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()

                        header_unwritten = False

                    for row_id, row in enumerate(reader):
                        record_id = filename + str(row_id)
                        cluster_details = cluster_membership.get(record_id, {})
                        row["source file"] = fileno
                        row.update(cluster_details)

                        writer.writerow(row)
