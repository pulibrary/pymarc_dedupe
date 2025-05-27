"""Module providing a function to write an xml or
json file of marc records to a Postgres database"""

import os.path
import time
import psycopg2
from pymarc import exceptions
from config import settings
from src.normalize.marc_record import MarcRecord
from src.handlers.streaming_json_handler import map_json
from src.handlers.streaming_xml_handler import map_xml
from src.normalize.gold_rush import GoldRush

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS records (
id TEXT,
title TEXT,
author TEXT,
publication_year TEXT,
pagination TEXT,
edition TEXT,
publisher_name TEXT,
type_of VARCHAR,
is_electronic_resource BOOL,
source_file TEXT,
goldrush TEXT,
UNIQUE (id)
);
"""

CREATE_RECORD_SQL = """INSERT INTO records VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

ADD_GOLDRUSH_COLUMN_SQL = """ALTER TABLE records
ADD goldrush text;
"""

ADD_GOLDRUSH_TO_RECORD_SQL = """UPDATE records
SET goldrush = %s
WHERE id = %s;
"""


class MarcToDb:
    conn = psycopg2.connect(
        database=settings.db_name,
        user=settings.db_user,
        host=settings.db_host,
        port=settings.db_port,
    )
    conn.autocommit = True

    @classmethod
    def find_or_create_table(cls):
        with cls.conn.cursor() as cur:
            try:
                cur.execute(CREATE_TABLE_SQL)
                cur.execute(ADD_GOLDRUSH_COLUMN_SQL)
            except psycopg2.DatabaseError:
                pass

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.conn = MarcToDb.conn
        self.source_file, self.file_extension = os.path.splitext(
            os.path.basename(self.input_file_path)
        )
        self.cursor = self.conn.cursor()

    def to_db(self):
        print(
            f"""time: {time.asctime(time.localtime())} -
                writing records in {self.input_file_path} to database
            """
        )
        if self.file_extension == ".xml":
            map_xml(self.add_record, self.input_file_path)
        elif self.file_extension == ".json":
            map_json(self.add_record, self.input_file_path)
        else:
            raise ValueError("Files must be either xml or json")

    def add_record(self, record):
        try:
            self.cursor.execute(CREATE_RECORD_SQL, self.record_data(record))
        except (psycopg2.DatabaseError, exceptions.MissingLinkedFields):
            mr = MarcRecord(record)
            self.cursor.execute(
                ADD_GOLDRUSH_TO_RECORD_SQL, (GoldRush(mr).as_gold_rush(), mr.id())
            )

    def record_data(self, record):
        mr = MarcRecord(record)
        return (
            mr.id(),
            mr.title() or None,
            mr.author() or None,
            mr.publication_year() or None,
            mr.pagination() or None,
            mr.edition() or None,
            mr.publisher_name() or None,
            mr.type_of() or None,
            mr.is_electronic_resource(),
            self.source_file,
            GoldRush(mr).as_gold_rush(),
        )
