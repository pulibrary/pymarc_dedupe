from src.link_records import LinkRecords


def test_importing_csv_file(example_dictionary):
    link_records = LinkRecords("tests/alma_marc_records_short.xml")
    link_records.save_marc_xml_as_csv()
    data_from_method = link_records.read_data()

    assert (
        data_from_method["tests/alma_marc_records_short.csv0"]
        == example_dictionary["tests/alma_marc_records_short.csv0"]
    )
    assert data_from_method == example_dictionary
