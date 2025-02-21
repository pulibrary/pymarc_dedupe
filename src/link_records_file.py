import csv
import os.path
from src.marc_to_csv import MarcToCsv


class LinkRecordsFile:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.csv_path = MarcToCsv(self.input_file_path).csv_path()
        if os.path.exists(self.csv_path):
            print("CSV file already present, not regenerating")
        else:
            self.save_marc_xml_as_csv()

    def save_marc_xml_as_csv(self):
        marc_to_csv = MarcToCsv(self.input_file_path)
        marc_to_csv.to_csv()

    def read_data(self):
        data_d = {}
        with open(self.csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                clean_row = {k: self.pre_process(v) for (k, v) in row.items()}
                data_d[self.csv_path + str(i)] = dict(clean_row)

        return data_d

    def pre_process(self, val):
        """
        Replace empty values with None
        """
        if not val:
            val = None
        return val
