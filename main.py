#!/usr/bin/python
import argparse
from src.link_records import LinkRecords

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PyMarc Dedupe",
        description="""Script that compares two Marc XML files
         to find duplicates using machine learning""",
    )
    parser.add_argument(
        "--file1",
        "-f1",
        required=True,
        type=str,
        help="the path to the first Marc Xml file for comparison",
    )
    parser.add_argument(
        "--file2",
        "-f2",
        required=True,
        type=str,
        help="the path to the second Marc Xml file for comparison",
    )
    parser.add_argument(
        "--dir",
        "-d",
        default="experiments_files_and_output",
        type=str,
        help="""the directory where %(prog)s will save settings,
         training, and data output files. (default: %(default)s)""",
    )
    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    output_dir = args.dir
    print("file1 is " + file1)
    print("file2 is " + file2)
    print("dir is " + output_dir)

    print("importing data ...")

    link_records = LinkRecords(file1, file2, output_dir)
    linker = link_records.linker()
    link_records.cluster(linker)
