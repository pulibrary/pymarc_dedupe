import pytest
from pymarc import parse_xml_to_array, Record, Field, Subfield


@pytest.fixture(scope="session", name="all_records")
def fixture_all_records():
    return parse_xml_to_array("alma_marc_records.xml")


@pytest.fixture(name="record_from_file")
def fixture_record_from_file(all_records):
    return all_records[0]


@pytest.fixture(name="record_with_description")
def fixture_record_with_description():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="300",
            subfields=[
                Subfield(code="a", value="578 p. ; "),
                Subfield(code="c", value="27 cm"),
            ],
        )
    )
    return pymarc_record


@pytest.fixture(name="record_with_short_title")
def fixture_record_with_short_title():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="245",
            subfields=[Subfield(code="a", value="Science :")],
        )
    )
    return pymarc_record


@pytest.fixture(name="record_with_title")
def fixture_record_with_title(record_with_short_title):
    record_with_short_title["245"].add_subfield(
        code="b", value="a poem dedicated etc. : and so forth"
    )
    return record_with_short_title


@pytest.fixture(name="record_with_title_and_subfield_p")
def fixture_record_with_title_and_subfield_p(record_with_title):
    record_with_title["245"].add_subfield(code="p", value="Labor unions")
    record_with_title["245"].add_subfield(code="p", value="Supplement /")
    return record_with_title
