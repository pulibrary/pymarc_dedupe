import csv
import dedupe
from src.link_records_file import LinkRecordsFile
from src.machine_learning_model import MachineLearningModel


class DedupeRecords(MachineLearningModel):
    def __init__(self, input_file, output_directory, match_threshold=0.5):
        super().__init__(output_directory, match_threshold)
        linked_records_file = LinkRecordsFile(input_file, True)
        self.input_file = linked_records_file.csv_path
        self.data_d = linked_records_file.read_data()

    def deduper(self):
        try:
            with open(self.settings_file_path, "rb") as sf:
                print("reading from", self.settings_file_path)
                model = dedupe.StaticDedupe(sf)
        except FileNotFoundError:
            model = dedupe.Dedupe(self.fields())
            model = self.train_and_write_model(model)

        return model

    # pylint: disable=duplicate-code
    def prepare_training(self, model):
        try:
            with open(self.training_file_path, encoding="utf-8") as tf:
                return model.prepare_training(
                    self.data_d, training_file=tf, sample_size=1500
                )
        except FileNotFoundError:
            return model.prepare_training(self.data_d, sample_size=1500)

    # pylint: enable=duplicate-code
    # pylint: disable=duplicate-code
    def cluster(self, model):
        print("clustering...")
        clustered_records = model.partition(self.data_d, self.match_threshold)
        print("# duplicate sets", len(clustered_records))

        cluster_membership = {}
        for cluster_id, (cluster, scores) in enumerate(clustered_records):
            for record_id, score in zip(cluster, scores):
                cluster_membership[record_id] = {
                    "Cluster ID": cluster_id,
                    "Link Score": score,
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
                "Cluster ID",
                "Link Score",
            ]
            filename = self.input_file
            with open(filename, encoding="utf-8") as f_input:
                reader = csv.DictReader(f_input)
                if header_unwritten:
                    writer = self.write_headers(f, additional_headers, reader)
                    header_unwritten = False

                for row_id, row in enumerate(reader):
                    record_id = row_id
                    self.update_row(cluster_membership, writer, row, record_id)

    # pylint: enable=duplicate-code
    # pylint: enable=possibly-used-before-assignment
