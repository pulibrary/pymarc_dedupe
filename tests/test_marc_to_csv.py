from src.marc_to_csv import MarcToCsv


def test_turning_marc_xml_to_csv():
    new_thing = MarcToCsv("tests/alma_marc_records.xml")
    new_thing.to_csv()
