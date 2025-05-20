from src.marc_to_db import MarcToDb


def test_turning_marc_xml_to_db():
    MarcToDb.find_or_create_table()
    new_thing = MarcToDb("tests/fixtures/for_db/alma_marc_records.xml")
    new_thing.to_db()

    sql = "SELECT * FROM records WHERE record_source = 'alma_marc_records';"
    with new_thing.conn.cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()
        assert (len(results)) == 122


def test_turning_marc_json_to_db():
    MarcToDb.find_or_create_table()
    new_thing = MarcToDb("tests/fixtures/for_db/marc_records.json")
    new_thing.to_db()
    new_thing.to_db()
    sql = "SELECT * FROM records WHERE record_source = 'marc_records';"
    with new_thing.conn.cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()
        assert (len(results)) == 7
