from src.marc_to_db import MarcToDb
# import psycopg2


def test_turning_marc_xml_to_db(db_config):
    new_thing = MarcToDb("tests/fixtures/alma_marc_records.xml", db_config)
    new_thing.to_db()
    # conn = psycopg2.connect(
    #     database=db_config["dbname"],
    #     user=db_config["user"],
    #     host=db_config["host"],
    #     port=db_config["port"],
    # )


def test_turning_marc_json_to_csv(db_config):
    new_thing = MarcToDb("tests/fixtures/marc_records.json", db_config)
    new_thing.to_db()
