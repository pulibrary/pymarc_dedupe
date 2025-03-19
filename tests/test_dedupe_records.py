from unittest.mock import patch

from src.dedupe_records import DedupeRecords


@patch("builtins.input")
def test_deduplicating_one_set_of_records(mocker, helpers, console_inputs, all_files):
    # Needed to mock interactive console
    mocker.side_effect = console_inputs
    test_file = "tests/fixtures/alma_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    helpers.file_cleanup(all_files)
    my_class = DedupeRecords(test_file, output_directory)
    model = my_class.deduper()
    my_class.cluster(model)
