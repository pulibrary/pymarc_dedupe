from unittest.mock import patch
from src.db_dedupe_records import DbDedupeRecords


@patch("builtins.input")
def test_deduplicating_directory_of_records(mocker, helpers, console_inputs, all_files):
    # Needed to mock interactive console
    mocker.side_effect = console_inputs
    input_directory = "tests/fixtures/for_db"
    output_directory = "tests/test_outputs"
    helpers.file_cleanup(all_files)
    my_class = DbDedupeRecords(input_directory, output_directory)
    model = my_class.deduper()
    my_class.block(model)
    my_class.cluster(model)
