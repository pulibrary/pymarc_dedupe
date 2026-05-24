"""Module for shared logic for Machine Learning models for deduplication.
Not intended to be used independently"""

import os.path
import csv
import dedupe


class MachineLearningModel:
    def __init__(self, output_directory, match_threshold=0.5):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self.output_file_path = os.path.join(
            output_directory, "data_matching_output.csv"
        )
        self.settings_file_path = os.path.join(
            output_directory, "data_matching_learned_settings"
        )
        self.training_file_path = os.path.join(
            output_directory, "data_matching_training.json"
        )
        self.match_threshold = match_threshold

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

    def train_and_write_model(self, model):
        self.prepare_training(model)
        self.console_label(model)
        model.train()
        # When finished, save our training away to disk
        self.write_training(model)
        self.write_settings(model)
        return model

    def prepare_training(self, _model):
        raise NotImplementedError("Must override prepare_training")

    def console_label(self, model):
        print("starting active labeling...")
        dedupe.console_label(model)

    def write_training(self, linker):
        with open(self.training_file_path, "w", encoding="utf-8") as tf:
            linker.write_training(tf)

    def write_settings(self, linker):
        with open(self.settings_file_path, "wb") as sf:
            linker.write_settings(sf)

    def write_headers(self, file, additional_headers, reader):
        fieldnames = additional_headers + reader.fieldnames

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        return writer

    def update_row(self, cluster_membership, writer, row, record_id):
        cluster_details = cluster_membership.get(record_id, {})
        row.update(cluster_details)
        writer.writerow(row)
