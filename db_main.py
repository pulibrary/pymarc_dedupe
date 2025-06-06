#!/usr/bin/python
import argparse
import time
from src.models.db_dedupe_records import DbDedupeRecords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PyMarc Dedupe",
        description="""Script that compares files in a directory of Marc XML or JSON files
         to find duplicates using machine learning""",
    )
    parser.add_argument(
        "--input_dir",
        "-i",
        required=True,
        type=str,
        help="the path to the directory of Marc XML or JSON files for comparison",
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        default="experiments_files_and_output",
        type=str,
        help="""the directory where %(prog)s will save settings,
         training, and data output files. (default: %(default)s)""",
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    print(f"time: {time.asctime(time.localtime())} - BEGIN")
    print("Input directory is " + input_dir)
    print("Output directory is " + output_dir)
    print(f"time: {time.asctime(time.localtime())} - importing data ...")

    my_class = DbDedupeRecords(input_dir, output_dir)
    model = my_class.deduper()
    my_class.block(model)
    my_class.cluster(model)
    my_class.create_table_for_csv()
    my_class.write_to_csv()
