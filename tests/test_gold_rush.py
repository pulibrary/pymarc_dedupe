from pymarc import Record, Field, Subfield
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush


def test_potentially_empty_fields(all_records):
    for record in all_records:
        new_record = MarcRecord(record)
        new_string = GoldRush(new_record)
        new_string.as_gold_rush()


def test_as_gold_rush(record_from_file):
    pymarc_record = record_from_file
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (
        (new_string.as_gold_rush())
        # pylint: disable=line-too-long
        == "scienceapoemdedicatedtotheamericanassociationfortheadvancementofscienc18561______vanbea_______________________________________________________stree_______________e"
        # pylint: enable=line-too-long
    )


def test_as_gold_rush_their_example():
    pymarc_record = Record(leader="03377cam a22006134i 4500")
    pymarc_record.add_field(
        Field(
            tag="100",
            subfields=[
                Subfield(code="a", value="Snyder, Timothy, "),
                Subfield(code="e", value="author."),
            ],
        ),
        Field(
            tag="245",
            subfields=[
                Subfield(code="a", value="On tyranny :"),
                Subfield(code="b", value="twenty lessons from the twentieth century /"),
                Subfield(code="c", value="Timothy Snyder."),
            ],
        ),
        Field(tag="008", data="170403s2017 nyu 000 0 eng "),
        Field(
            tag="300",
            subfields=[
                Subfield(code="a", value="126 pages ;"),
                Subfield(code="c", value="16 cm"),
            ],
        ),
        Field(tag="250", subfields=[Subfield(code="a", value="First edition.")]),
        Field(
            tag="260",
            subfields=[
                Subfield(code="a", value="New York :"),
                Subfield(code="b", value="Tim Duggan Books, "),
                Subfield(code="c", value="[2017]"),
            ],
        ),
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    # Their first field seems to have 75 characters, not 70, in their example, but the text says 70.
    # They have underscores after the year instead of page numbers
    # They have no space in the publisher, even though it says not to remove them
    assert (
        (new_string.as_gold_rush())
        # pylint: disable=line-too-long
        == "ontyrannytwentylessonsfromthetwentiethcentury_________________________2017126_1__timdua_______________________________________________________snyde_______________p"
        # pylint: enable=line-too-long
    )  # snyde_______________p'


def test_title():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="245", subfields=[Subfield(code="a", value="Short title")])
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (
        new_string.title()
    ) == "shorttitle____________________________________________________________"


def test_long_title(record_with_title_and_subfield_p):
    new_record = MarcRecord(record_with_title_and_subfield_p)
    new_string = GoldRush(new_record)
    assert (
        new_string.title()
    ) == "scienceapoemdedicatedetcandsoforthlaborunions_________________________"


def test_pagination(record_with_description):
    new_record = MarcRecord(record_with_description)
    new_string = GoldRush(new_record)
    assert (new_string.pagination()) == "578_"


def test_pagination_record(record_from_file):
    pymarc_record = record_from_file
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.pagination()) == "1___"


def test_publisher():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="260", subfields=[Subfield(code="b", value="U.S. Geological Survey ;")]
        )
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.publisher_name()) == "usgeo"


def test_empty_publisher():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.publisher_name()) == "_____"


def test_edition_as_gold_rush():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="250", subfields=[Subfield(code="a", value="2nd Ed.")])
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.edition()) == "2__"


def test_edition_as_gold_rush_alpha():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(tag="250", subfields=[Subfield(code="a", value="First edition")])
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.edition()) == "1__"


def test_empty_edition_as_gold_rush():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.edition()) == "___"


def test_strip_punctuation():
    pymarc_record = Record()
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.strip_punctuation(" & ")) == "and"
    assert (new_string.strip_punctuation("'{ }")) == "_"
    #
    assert (new_string.strip_punctuation("!()\\-©")) == "______"
    assert (new_string.strip_punctuation("  and  Another ")) == "and_another"
    assert (new_string.strip_punctuation("The Title ")) == "title"


def test_title_inclusive_dates():
    pymarc_record = Record()
    pymarc_record.add_field(
        Field(
            tag="245",
            subfields=[Subfield(code="f", value="1903 Sept. 16-1907 Oct. 5.")],
        )
    )
    new_record = MarcRecord(pymarc_record)
    new_string = GoldRush(new_record)
    assert (new_string.title_inclusive_dates()) == "1903_sept__16_1"


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
    new_string = GoldRush(new_record)
    assert (new_string.author()) == "jacqu"
