from os import makedirs
from unittest.mock import patch
from pytest import raises
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
    model = my_class.deduper()


# pylint: disable=duplicate-code
@patch("builtins.input")
def test_prepare_training_data(mocker, helpers, console_inputs):
    mocker.side_effect = console_inputs
    files = [
        "tests/test_outputs/data_matching_learned_settings",
        "tests/test_outputs/data_matching_output.csv",
    ]
    helpers.file_cleanup(files)
    input_directory = "tests/fixtures/for_db"
    output_directory = "tests/test_outputs"
    my_class = DbDedupeRecords(input_directory, output_directory)
    model = my_class.deduper()
    my_class.block(model)
    my_class.cluster(model)
    # pylint: enable=duplicate-code


def test_with_an_empty_input_dir(helpers, all_files):
    helpers.file_cleanup(all_files)
    input_directory = "tests/fixtures/empty_on_purpose"
    makedirs(input_directory, exist_ok=True)
    output_directory = "tests/test_outputs"
    with raises(ValueError):
        DbDedupeRecords(input_directory, output_directory)
