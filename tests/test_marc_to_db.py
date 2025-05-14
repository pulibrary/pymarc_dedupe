import psycopg2
from src.marc_to_db import MarcToDb


def test_turning_marc_xml_to_db(db_config):
    new_thing = MarcToDb("tests/fixtures/alma_marc_records.xml")
    new_thing.to_db()
    conn = psycopg2.connect(
        database=db_config["dbname"],
        user=db_config["user"],
        host=db_config["host"],
        port=db_config["port"],
    )
    sql = "SELECT * FROM records WHERE record_source = 'alma_marc_records';"
    with conn.cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()
        assert (len(results)) == 122


def test_turning_marc_json_to_db(db_config):
    new_thing = MarcToDb("tests/fixtures/marc_records.json")
    new_thing.to_db()
    new_thing.to_db()
    conn = psycopg2.connect(
        database=db_config["dbname"],
        user=db_config["user"],
        host=db_config["host"],
        port=db_config["port"],
    )
    sql = "SELECT * FROM records WHERE record_source = 'marc_records';"
    with conn.cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()
        assert (len(results)) == 7
