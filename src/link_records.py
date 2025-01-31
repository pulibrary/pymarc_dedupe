import csv
from src.marc_to_csv import MarcToCsv

# import os.path
# from pymarc import parse_xml_to_array
# from src.marc_record import MarcRecord


class LinkRecords:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.csv_path = MarcToCsv(self.input_file_path).csv_path

    def save_marc_xml_as_csv(self):
        marc_to_csv = MarcToCsv(self.input_file_path)
        marc_to_csv.to_csv()

    def read_data(self):
        data_d = {}
        with open(self.csv_path(), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # clean_row = {k: v for (k, v) in row.items()}
                data_d[self.csv_path() + str(i)] = dict(row)

        return data_d
