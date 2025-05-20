import os.path
import psycopg2
from pymarc import map_xml, parse_json_to_array
from config import settings
from src.marc_record import MarcRecord

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
record_source TEXT,
UNIQUE (id)
);
"""

CREATE_RECORD_SQL = """INSERT INTO records VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            cur.execute(CREATE_TABLE_SQL)

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.conn = MarcToDb.conn
        self.record_source, self.file_extension = os.path.splitext(
            os.path.basename(self.input_file_path)
        )
        self.cursor = self.conn.cursor()

    def to_db(self):
        if self.file_extension == ".xml":
            map_xml(self.add_record, self.input_file_path)
        elif self.file_extension == ".json":
            for record in parse_json_to_array(self.input_file_path):
                self.add_record(record)

    def add_record(self, record):
        mr = MarcRecord(record)

        data = (
            mr.id(),
            mr.title() or None,
            mr.author() or None,
            mr.publication_year() or None,
            mr.pagination() or None,
            mr.edition() or None,
            mr.publisher_name() or None,
            mr.type_of() or None,
            mr.is_electronic_resource(),
            self.record_source,
        )
        try:
            self.cursor.execute(CREATE_RECORD_SQL, data)
        except psycopg2.DatabaseError:
            pass
