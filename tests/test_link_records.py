import os
from src.link_records import LinkRecords


def test_comparing_two_sets_of_records():
    left_file = "tests/alma_marc_records_short.xml"
    right_file = "tests/hl_marc_records_short.xml"
    output_directory = "tests/test_outputs"
    linker = LinkRecords(left_file, right_file, output_directory)
    # delete any previous test files
    files = [linker.settings_file, linker.output_file, linker.training_file]
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
    linker.fields()
    linker.linker()
    linker.prepare_training()
