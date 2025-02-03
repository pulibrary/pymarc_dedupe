import os
from unittest.mock import patch

from src.link_records import LinkRecords


@patch("builtins.input")
def test_comparing_two_sets_of_records(mocker):
    # Needed to mock interactive console
    inputs = [
        "n",
        "y",
        "n",
        "n",
        "y",
        "y",
        "n",
        "n",
        "y",
        "y",
        "y",
        "y",
        "y",
        "y",
        "y",
        "f",
    ]
    mocker.side_effect = inputs
    left_file = "tests/alma_marc_records_short.xml"
    right_file = "tests/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    linker = LinkRecords(left_file, right_file, output_directory)
    # delete any previous test files
    files = [
        linker.settings_file_path,
        linker.output_file_path,
        linker.training_file_path,
    ]
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    linker.fields()
    linker.linker()


# Training data created in test above
def test_comparing_two_sets_of_records_with_pre_existing_training_data():
    left_file = "tests/alma_marc_records_short.xml"
    right_file = "tests/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    linker = LinkRecords(left_file, right_file, output_directory)
    linker.linker()


def test_clustering_with_pre_existing_training_data():
    left_file = "tests/alma_marc_records_short.xml"
    right_file = "tests/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    link_records = LinkRecords(left_file, right_file, output_directory)
    linker = link_records.linker()
    link_records.cluster(linker)
