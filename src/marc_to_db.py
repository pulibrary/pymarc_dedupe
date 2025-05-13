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
gold_rush TEXT
);
"""

RECORD_SQL = """INSERT INTO records VALUES
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                )
                cur.execute(RECORD_SQL, data)

    def pymarc_records_from_file(self):
        try:
            return parse_xml_to_array(self.input_file_path)
        except SAXParseException:
            return parse_json_to_array(self.input_file_path)
