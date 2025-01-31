import os
from src.link_records_file import LinkRecordsFile


def test_importing_xml_file(example_dictionary):
    os.remove("tests/alma_marc_records_short.csv")
    link_records = LinkRecordsFile("tests/alma_marc_records_short.xml")
    data_from_method = link_records.read_data()

    assert data_from_method == example_dictionary


def test_when_a_csv_already_exists(example_dictionary):
    LinkRecordsFile("tests/alma_marc_records_short.xml")
    link_records = LinkRecordsFile("tests/alma_marc_records_short.xml")
    data_from_method = link_records.read_data()
    assert data_from_method == example_dictionary
