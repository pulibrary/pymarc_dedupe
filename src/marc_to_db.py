import os.path
from xml.sax import SAXParseException
import psycopg2
from pymarc import parse_xml_to_array
from pymarc import parse_json_to_array
from config import settings
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS records (
id TEXT,
title TEXT,
transliterated_title TEXT,
publication_year TEXT,
pagination TEXT,
edition TEXT,
publisher_name TEXT,
type_of VARCHAR,
title_part TEXT,
title_number TEXT,
author TEXT,
title_inclusive_dates TEXT,
gov_doc_number TEXT,
is_electronic_resource BOOL,
gold_rush TEXT,
record_source TEXT
);
"""

CREATE_RECORD_SQL = """INSERT INTO records VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

FIND_RECORD_SQL = """SELECT * FROM records WHERE id = (%s);
"""


class MarcToDb:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.conn = psycopg2.connect(
            database=settings.db_name,
            user=settings.db_user,
            host=settings.db_host,
            port=settings.db_port,
        )
        self.conn.autocommit = True
        self.find_or_create_table()

    def to_db(self):
        with self.conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            for record in self.pymarc_records_from_file():
                mr = MarcRecord(record)
                # this requires 1 to 2 database queries per record,
                # which is probably making this slow
                # could we create an array of record IDs from the database at the beginning
                # and then check the record ID against that array?
                cur.execute("SELECT * FROM records WHERE id = (%s)", (mr.id(),))
                result = cur.fetchall()
                if len(result) > 0:
                    continue

                record_source, _file_extension = os.path.splitext(
                    os.path.basename(self.input_file_path)
                )
                data = (
                    mr.id(),
                    mr.title() or None,
                    mr.transliterated_title() or None,
                    mr.publication_year() or None,
                    mr.pagination() or None,
                    mr.edition() or None,
                    mr.publisher_name() or None,
                    mr.type_of() or None,
                    mr.title_part() or None,
                    mr.title_number() or None,
                    mr.author() or None,
                    mr.title_inclusive_dates() or None,
                    mr.gov_doc_number() or None,
                    mr.is_electronic_resource(),
                    GoldRush(mr).as_gold_rush(),
                    record_source,
                )

                cur.execute(CREATE_RECORD_SQL, data)

    def pymarc_records_from_file(self):
        # I think for big files we're going to need something else here
        # I think this requires putting the whole file in memory
        # We could do the file in chunks?
        try:
            return parse_xml_to_array(self.input_file_path)
        except SAXParseException:
            return parse_json_to_array(self.input_file_path)

    def find_or_create_table(self):
        with self.conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
