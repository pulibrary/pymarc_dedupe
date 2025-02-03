import os.path
import dedupe
from src.link_records_file import LinkRecordsFile


class LinkRecords:
    def __init__(self, left_file, right_file, output_directory):
        self.left_data = LinkRecordsFile(left_file).read_data()
        self.right_data = LinkRecordsFile(right_file).read_data()
        self.output_file = os.path.join(output_directory, "data_matching_output.csv")
        self.settings_file = os.path.join(
            output_directory, "data_matching_learned_settings"
        )
        self.training_file = os.path.join(
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
            with open(self.settings_file, "rb") as sf:
                return dedupe.StaticRecordLink(sf)
        except FileNotFoundError:
            return dedupe.RecordLink(self.fields())

    def prepare_training(self):
        try:
            with open(self.training_file, encoding="utf-8") as tf:
                self.linker().prepare_training(
                    self.left_data, self.right_data, training_file=tf, sample_size=1500
                )
        except FileNotFoundError:
            self.linker().prepare_training(
                self.left_data, self.right_data, sample_size=1500
            )
