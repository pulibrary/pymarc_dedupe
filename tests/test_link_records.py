import shutil
from unittest.mock import patch

from src.link_records import LinkRecords


@patch("builtins.input")
def test_comparing_two_sets_of_records(mocker, helpers, console_inputs, all_files):
    # Mock interactive console
    mocker.side_effect = console_inputs
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    helpers.file_cleanup(all_files)
    linker = LinkRecords(left_file, right_file, output_directory)
    linker.fields()
    linker.linker()


# Training data created in test above
def test_comparing_two_sets_of_records_with_pre_existing_training_data():
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    linker = LinkRecords(left_file, right_file, output_directory)
    linker.linker()


def test_clustering_with_pre_existing_training_data():
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    link_records = LinkRecords(left_file, right_file, output_directory)
    linker = link_records.linker()
    link_records.cluster(linker)


@patch("builtins.input")
def test_prepare_training_data(mocker, helpers, console_inputs):
    # Mock interactive console
    mocker.side_effect = console_inputs
    # delete any previous test files, other than training data
    files = [
        "tests/test_outputs/data_matching_learned_settings",
        "tests/test_outputs/data_matching_output.csv",
    ]
    helpers.file_cleanup(files)
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    link_records = LinkRecords(left_file, right_file, output_directory)
    linker = link_records.linker()
    link_records.prepare_training(linker)


@patch("builtins.input")
def test_comparing_two_sets_of_records_with_json(
    mocker, helpers, console_inputs, all_files
):
    # Mock interactive console
    mocker.side_effect = console_inputs
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/marc_records.json"
    output_directory = "tests/test_outputs"
    helpers.file_cleanup(all_files)
    linker = LinkRecords(left_file, right_file, output_directory)
    linker.fields()
    linker.linker()


def test_creating_dir():
    output_directory = "tests/test_outputs"
    left_file = "tests/fixtures/alma_marc_records_short.xml"
    right_file = "tests/fixtures/marc_records.json"
    shutil.rmtree(output_directory, ignore_errors=True)
    LinkRecords(left_file, right_file, output_directory)
