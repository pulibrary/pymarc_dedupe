from pymarc import Record, Field, Subfield
from src.marc_record import MarcRecord


def test_against_real_data(all_records):
    for record in all_records:
        new_record = MarcRecord(record)
        new_record.to_dictionary()


def test_empty_record():
    # We shouldn't actually get empty records, but this will tell us whether,
    # if any one field is empty, our code will error
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    new_record.to_dictionary()


def test_two_valid_dates_publication_year():
    # If both date_one and date_two are valid dates, use date_two
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s19842006nyu     o     000 p eng d"),
        Field(tag="260", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    # If date_two is blank, use date_one
    assert (new_record.publication_year()) == 2006


def test_blank_date_two_publication_year():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s1984    nyu     o     000 p eng d"),
        Field(tag="260", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    # If date_two is blank, use date_one
    assert (new_record.publication_year()) == 1984


def test_nines_publication_year():
    # If date_two is 9999, use date_one
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s19849999nyu     o     000 p eng d"),
        Field(tag="260", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publication_year()) == 1984


def test_too_short_publication_year():
    # If date_two does not have 4 digits, use date_one
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s1984200 nyu     o     000 p eng d"),
        Field(tag="260", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publication_year()) == 1984


def test_from_264_publication_year():
    # If neither date_one nor date_two are valid dates, use date from 264$c
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s198 200 nyu     o     000 p eng d"),
        Field(tag="264", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publication_year()) == 1999


def test_from_260_publication_year():
    # If neither date_one nor date_two are valid dates, use date from 264$c
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s198 200 nyu     o     000 p eng d"),
        Field(tag="260", subfields=[Subfield(code="c", value="1999.")]),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publication_year()) == 1999


def test_date_one():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s1856    nyu     o     000 p eng d")
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.date_one()) == 1856


def test_date_two():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="008", data="020506s1856    nyu     o     000 p eng d")
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.date_two()) == ""


# pylint: disable=protected-access
def test_date_of_production():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record._MarcRecord__date_of_production()) == ""


def test_date_of_publication():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="260", subfields=[Subfield(code="c", value="1856.")])
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record._MarcRecord__date_of_publication()) == 1856


def test_empty_date_of_publication():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record._MarcRecord__date_of_publication()) == ""


# pylint: enable=protected-access


def test_is_valid_date_only_spaces():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert not new_record.is_valid_date("    ")


def test_title(record_with_title_and_subfield_p):
    new_record = MarcRecord(record_with_title_and_subfield_p)
    assert (
        new_record.title()
    ) == "Science : a poem dedicated etc. : and so forth Labor unions"


def test_empty_transliterated_title():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record.transliterated_title()) == ""


def test_empty_title():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record.title()) == ""


# pylint: disable=duplicate-code
def test_vernacular_title():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="245",
            # pylint: enable=duplicate-code
            subfields=[
                Subfield(code="6", value="880-01"),
                Subfield(code="a", value="Xin shi san bai shou bai nian xin bian / "),
            ],
        ),
        Field(
            tag="880",
            subfields=[
                Subfield(code="6", value="245-01/$1"),
                Subfield(code="a", value="新诗三百首百年新编 / "),
            ],
        ),
        Field(
            tag="100",
            subfields=[
                Subfield(code="6", value="880-02"),
                Subfield(code="a", value="Chatzēantōniou, Kōstas, "),
            ],
        ),
        Field(
            tag="880",
            subfields=[
                Subfield(code="6", value="100-02/(S)"),
                Subfield(code="a", value="Χατζηαντωνίου, Κωστας, "),
            ],
        ),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.title()) == "新诗三百首百年新编"


def test_title_no_subfield_p(record_with_title):
    new_record = MarcRecord(record_with_title)
    assert (new_record.title()) == "Science : a poem dedicated etc. : and so forth"


# pylint: disable=protected-access
def test_strip_punctuation():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (
        new_record._MarcRecord__strip_punctuation("My : fake title ")
    ) == "My fake title"


# pylint: enable=protected-access


def test_pagination(record_with_description):
    record_with_description["300"]["a"] = "578 pages ; "
    new_record = MarcRecord(record_with_description)
    assert (new_record.pagination()) == "578 pages"


def test_normalize_pagination(record_with_description):
    new_record = MarcRecord(record_with_description)
    assert (new_record.pagination()) == "578 pages"


# pylint: disable=protected-access
def test_normalize_extent():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record._MarcRecord__normalize_extent("57 p. ; ")) == "57 pages"
    assert (new_record._MarcRecord__normalize_extent("57 pages ; ")) == "57 pages"
    assert (new_record._MarcRecord__normalize_extent("3 v. ; ")) == "3 volumes"
    assert (new_record._MarcRecord__normalize_extent("3 volumes ; ")) == "3 volumes"
    assert (new_record._MarcRecord__normalize_extent("3 vol. ; ")) == "3 volumes"
    assert (new_record._MarcRecord__normalize_extent("4 ℓ.")) == "4 leaves"


# pylint: enable=protected-access


def test_edition_statement():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="250", subfields=[Subfield(code="a", value="2nd Ed.")])
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.edition()) == "2nd Edition"


def test_publisher_name_264():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="264",
            subfields=[Subfield(code="b", value="Doubleday & Company, Inc., ")],
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publisher_name()) == "Doubleday & Company Inc"


def test_publisher_name_260():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="260",
            subfields=[Subfield(code="b", value="Doubleday & Company, Inc., ")],
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publisher_name()) == "Doubleday & Company Inc"


def test_empty_publisher_name():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert (new_record.publisher_name()) == ""


def test_type_of():
    pymarc_record = Record(leader="00475cas a2200169 i 4500")
    new_record = MarcRecord(pymarc_record)
    assert (new_record.type_of()) == "a"


def test_title_part(record_with_title_and_subfield_p):
    record_with_title_and_subfield_p["245"].add_subfield(
        code="p", value="Another subpart / "
    )
    new_record = MarcRecord(record_with_title_and_subfield_p)
    assert (new_record.title_part()) == "Supplement Another subpart"


def test_title_number(record_with_short_title):
    record_with_short_title["245"].add_subfield(code="n", value="Book 1 : ")
    new_record = MarcRecord(record_with_short_title)
    assert (new_record.title_number()) == "Book 1"


def test_author():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="100",
            subfields=[
                Subfield(code="a", value="Jacquet de La Guerre, Elisabeth-Claude, ")
            ],
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.author()) == "Jacquet de La Guerre, Elisabeth-Claude"


def test_vernacular_author():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="245",
            subfields=[
                Subfield(code="6", value="880-01"),
                Subfield(code="a", value="Xin shi san bai shou bai nian xin bian / "),
            ],
        ),
        Field(
            tag="880",
            subfields=[
                Subfield(code="6", value="245-01/$1"),
                Subfield(code="a", value="新诗三百首百年新编 / "),
            ],
        ),
        Field(
            tag="100",
            subfields=[
                Subfield(code="6", value="880-02"),
                Subfield(code="a", value="Chatzēantōniou, Kōstas, "),
            ],
        ),
        Field(
            tag="880",
            subfields=[
                Subfield(code="6", value="100-02/(S)"),
                Subfield(code="a", value="Χατζηαντωνίου, Κωστας, "),
            ],
        ),
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.author()) == "Χατζηαντωνίου, Κωστας"


# This might be weird behavior?
def test_number_of_characters():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert not new_record.number_of_characters(1982)


def test_corp_author():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="110", subfields=[Subfield(code="a", value="Lexus (Firm : Peru).")])
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.author()) == "Lexus (Firm : Peru)"


def test_meeting_name_author():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="111",
            subfields=[
                Subfield(
                    code="a",
                    # pylint: disable=line-too-long
                    value="Colloque Voyages et conscience patrimoniale, Aubin-Louis Millin (1759-1818) entre France et Italie ",
                    # pylint: enable=line-too-long
                )
            ],
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert (
        (new_record.author())
        # pylint: disable=line-too-long
        == "Colloque Voyages et conscience patrimoniale, Aubin-Louis Millin (1759-1818) entre France et Italie"
        # pylint: enable=line-too-long
    )


def test_title_inclusive_dates():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="245",
            subfields=[Subfield(code="f", value="1903 Sept. 16-1907 Oct. 5.")],
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.title_inclusive_dates()) == "1903 Sept. 16-1907 Oct. 5"


def test_gov_doc_number():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="086", subfields=[Subfield(code="a", value="HP40-71/2012F-PDF")])
    )
    new_record = MarcRecord(pymarc_record)
    assert (new_record.gov_doc_number()) == "HP40-71/2012F-PDF"


# pylint: disable=protected-access
def test_is_electronic_resource_245():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="245", subfields=[Subfield(code="h", value="[electronic resource]")])
    )
    new_record = MarcRecord(pymarc_record)
    assert new_record.is_electronic_resource()


def test_is_electronic_resource_reproduction():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="533", subfields=[Subfield(code="a", value="Electronic reproduction")]
        )
    )
    new_record = MarcRecord(pymarc_record)
    assert new_record.is_electronic_resource()


def test_is_electronic_resource_description(record_with_description):
    record_with_description["300"]["a"] = "1 online resource (iii, 447 pages) : "
    record_with_description["300"].delete_subfield("c")
    new_record = MarcRecord(record_with_description)
    assert new_record._MarcRecord__is_electronic_resource_from_description()
    assert new_record.is_electronic_resource()


def test_is_electronic_resource_from_007_c():
    pymarc_record = Record()
    pymarc_record.add_field(Field(tag="007", data="c"))
    new_record = MarcRecord(pymarc_record)
    assert new_record._MarcRecord__is_electronic_resource_from_007()
    assert new_record.is_electronic_resource()


def test_is_electronic_resource_from_007_d():
    pymarc_record = Record()
    pymarc_record.add_field(Field(tag="007", data="d"))
    new_record = MarcRecord(pymarc_record)
    assert not new_record._MarcRecord__is_electronic_resource_from_007()
    assert not new_record.is_electronic_resource()


def test_is_electronic_resource_when_not_e():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    assert not new_record._MarcRecord__is_electronic_resource_from_title()
    assert not new_record._MarcRecord__is_electronic_resource_from_reproduction()
    assert not new_record._MarcRecord__is_electronic_resource_from_description()
    assert not new_record._MarcRecord__is_electronic_resource_from_007()
    assert not new_record.is_electronic_resource()


# pylint: enable=protected-access
