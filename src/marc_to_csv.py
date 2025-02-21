import csv
import os.path
from pymarc import parse_xml_to_array
from src.marc_record import MarcRecord


class MarcToCsv:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def to_csv(self):
        output_file = self.csv_path()
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = self.records()[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records():
                writer.writerow(record)

    def pymarc_records_from_file(self):
        return parse_xml_to_array(self.input_file_path)

    def records(self):
        list_of_record_dictionaries = []
        for record in self.pymarc_records_from_file():
            mr = MarcRecord(record)
            list_of_record_dictionaries.append(mr.to_dictionary())
        return list_of_record_dictionaries

    def csv_path(self):
        filename, _file_extension = os.path.splitext(self.input_file_path)
        output_file = filename + ".csv"
        return output_file
