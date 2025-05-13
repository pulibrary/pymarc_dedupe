import os.path
from xml.sax import SAXParseException
import psycopg2
from pymarc import parse_xml_to_array
from pymarc import parse_json_to_array
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush

CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS records (
id TEXT,
title TEXT,
transliterated_title TEXT,
publication_year INT,
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
    def __init__(self, input_file_path, db_config):
        self.input_file_path = input_file_path
        self.conn = psycopg2.connect(
            database=db_config["dbname"],
            user=db_config["user"],
            host=db_config["host"],
            port=db_config["port"],
        )

    def to_db(self):
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            for record in self.pymarc_records_from_file():
                mr = MarcRecord(record)
                cur.execute("SELECT * FROM records WHERE id = (%s)", (mr.id(),))
                result = cur.fetchall()
                if len(result) > 0:
                    continue

                record_source, _file_extension = os.path.splitext(
                    os.path.basename(self.input_file_path)
                )
                data = (
                    mr.id(),
                    mr.title(),
                    mr.transliterated_title(),
                    mr.publication_year(),
                    mr.pagination(),
                    mr.edition(),
                    mr.publisher_name(),
                    mr.type_of(),
                    mr.title_part(),
                    mr.title_number(),
                    mr.author(),
                    mr.title_inclusive_dates(),
                    mr.gov_doc_number(),
                    mr.is_electronic_resource(),
                    GoldRush(mr).as_gold_rush(),
                    record_source,
                )
                cur.execute(CREATE_RECORD_SQL, data)

    def pymarc_records_from_file(self):
        try:
            return parse_xml_to_array(self.input_file_path)
        except SAXParseException:
            return parse_json_to_array(self.input_file_path)
