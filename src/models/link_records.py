import csv
import dedupe
from src.normalize.link_records_file import LinkRecordsFile
from src.models.machine_learning_model import MachineLearningModel


class LinkRecords(MachineLearningModel):
    def __init__(self, left_file, right_file, output_directory, match_threshold=0.5):
        super().__init__(output_directory, match_threshold)
        left_linked_records_file = LinkRecordsFile(left_file)
        right_linked_records_file = LinkRecordsFile(right_file)
        self.left_file = left_linked_records_file.csv_path
        self.right_file = right_linked_records_file.csv_path
        self.left_data = left_linked_records_file.read_data()
        self.right_data = right_linked_records_file.read_data()

    def linker(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print("reading from", self.settings_file_path)
                model = dedupe.StaticRecordLink(sf)
        except FileNotFoundError:
            model = dedupe.RecordLink(self.fields())
            model = self.train_and_write_model(model)

        return model

    # pylint: disable=duplicate-code
    def prepare_training(self, model):
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                return model.prepare_training(
                    self.left_data, self.right_data, training_file=tf, sample_size=1500
                )
        except FileNotFoundError:
            return model.prepare_training(
                self.left_data, self.right_data, sample_size=1500
            )

    # pylint: enable=duplicate-code
    # pylint: disable=duplicate-code
    def cluster(self, model):
        print("clustering...")
        clustered_records = model.join(
            self.left_data, self.right_data, self.match_threshold, "many-to-many"
        )
        print("# duplicate sets", len(clustered_records))

        cluster_membership = {}
        for cluster_id, (cluster, score) in enumerate(clustered_records):
            for record_id in cluster:
                cluster_membership[record_id] = {
                    "cluster_id": cluster_id,
                    "cluster_score": score,
                }
        self.write_output(cluster_membership)

    # pylint: enable=duplicate-code

    # pylint: disable=duplicate-code
    # pylint: disable=possibly-used-before-assignment
    def write_output(self, cluster_membership):
        print("Writing duplicates to output file path: " + self.output_file_path)
        with open(self.output_file_path, "w", encoding="utf-8") as f:
            header_unwritten = True
            additional_headers = [
                "cluster_id",
                "cluster_score",
                "source_file",
            ]
            for fileno, filename in enumerate((self.left_file, self.right_file)):
                with open(filename, encoding="utf-8") as f_input:
                    reader = csv.DictReader(f_input)
                    if header_unwritten:
                        writer = self.write_headers(f, additional_headers, reader)
                        header_unwritten = False

                    for row_id, row in enumerate(reader):
                        record_id = filename + str(row_id)
                        row["source_file"] = fileno
                        self.update_row(cluster_membership, writer, row, record_id)

    # pylint: enable=duplicate-code
    # pylint: enable=possibly-used-before-assignment
