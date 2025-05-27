from src.handlers.streaming_xml_handler import StreamingXmlHandler, parse_xml


def test_streaming_xml_handler():
    parse_xml("tests/fixtures/alma_marc_records.xml", StreamingXmlHandler(strict=True))
    parse_xml(
        "tests/fixtures/alma_marc_records.xml",
        StreamingXmlHandler(normalize_form="NFC"),
    )
