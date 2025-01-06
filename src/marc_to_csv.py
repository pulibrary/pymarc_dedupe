import csv
from pymarc import parse_xml_to_array
from src.marc_record import MarcRecord


class MarcToCsv:
    def __init__(self, file_path):
        self.file_path = file_path

    def to_csv(self):
        with open("marc_xml_as_csv.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = self.records()[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records():
                writer.writerow(record)

    def pymarc_records_from_file(self):
        return parse_xml_to_array(self.file_path)

    def records(self):
        list_of_record_dictionaries = []
        for record in self.pymarc_records_from_file():
            mr = MarcRecord(record)
            list_of_record_dictionaries.append(mr.to_dictionary())
        return list_of_record_dictionaries
