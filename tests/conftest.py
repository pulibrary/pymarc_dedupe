import os
import pytest
from pymarc import parse_xml_to_array, Record, Field, Subfield


@pytest.fixture(scope="session", name="all_records")
def fixture_all_records():
    return parse_xml_to_array("tests/fixtures/alma_marc_records.xml")


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


# pylint: disable=line-too-long
@pytest.fixture(name="example_dictionary")
def fixture_example_dictionary():
    return {
        "tests/fixtures/alma_marc_records_short.csv0": {
            "id": "99129089206406421",
            "title": "Science : a poem dedicated to the American Association for the Advancement of Science : Albany, August 28, 1856",
            "transliterated_title": "Science : a poem dedicated to the American Association for the Advancement of Science : Albany, August 28, 1856",
            "publication_year": "1856",
            "pagination": "1 online resource 9 pages",
            "edition": None,
            "publisher_name": "Van Benthuysen Printer",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Street, Alfred Billings",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "scienceapoemdedicatedtotheamericanassociationfortheadvancementofscienc18561______vanbea_______________________________________________________stree_______________e",
        },
        "tests/fixtures/alma_marc_records_short.csv1": {
            "id": "99129089203406421",
            "title": "Science : a poem",
            "transliterated_title": "Science : a poem",
            "publication_year": "1762",
            "pagination": "1 online resource iv 519 pages",
            "edition": None,
            "publisher_name": "Printed by William Dunlap in Marketstreet",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Hopkinson, Francis",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "scienceapoem__________________________________________________________17621______printa_______________________________________________________hopki_______________e",
        },
        "tests/fixtures/alma_marc_records_short.csv2": {
            "id": "99127156263806421",
            "title": "Science : evidence, truth & integrity",
            "transliterated_title": "Science : evidence, truth & integrity",
            "publication_year": "1985",
            "pagination": "1 online resource",
            "edition": None,
            "publisher_name": "US Dept of Commerce National Institute of Standards and Technology",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Passaglia, Elio",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "scienceevidencetruthandintegrity______________________________________19851______usdepa_______________________________________________________passa_______________e",
        },
        "tests/fixtures/alma_marc_records_short.csv3": {
            "id": "99127149995506421",
            "title": "Mineral resources of the Joyce Kilmer-Slickrock Wilderness, North Carolina-Tennessee",
            "transliterated_title": "Mineral resources of the Joyce Kilmer-Slickrock Wilderness, North Carolina-Tennessee",
            "publication_year": "1977",
            "pagination": "1 online resource vii 89 pages 3 pages of plates",
            "edition": None,
            "publisher_name": "United States Department of the Interior Geological Survey",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Lesure, Frank Gardner",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "mineralresourcesofthejoycekilmerslickrockwildernessnorthcarolinatennes19771______unitea_______________________________________________________lesur_______________e",
        },
        "tests/fixtures/alma_marc_records_short.csv4": {
            "id": "99125448801706421",
            "title": "Joyce Kilmer: Poems, Essays and Letters in Two Volumes. Volume 1, Memoirs and Poems",
            "transliterated_title": "Joyce Kilmer: Poems, Essays and Letters in Two Volumes. Volume 1, Memoirs and Poems",
            "publication_year": "2021",
            "pagination": None,
            "edition": None,
            "publisher_name": "Project Gutenberg",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Kilmer, Joyce",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "False",
            "gold_rush": "joycekilmerpoemsessaysandlettersintwovolumesvolume1memoirsandpoems____2021_______projea_______________________________________________________kilme_______________p",
        },
        "tests/fixtures/alma_marc_records_short.csv5": {
            "id": "99125448757506421",
            "title": "Dreams and Images: An Anthology of Catholic Poets",
            "transliterated_title": "Dreams and Images: An Anthology of Catholic Poets",
            "publication_year": "2021",
            "pagination": None,
            "edition": None,
            "publisher_name": "Project Gutenberg",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Kilmer, Joyce",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "False",
            "gold_rush": "dreamsandimagesananthologyofcatholicpoets_____________________________2021_______projea_______________________________________________________kilme_______________p",
        },
        "tests/fixtures/alma_marc_records_short.csv6": {
            "id": "99125448516306421",
            "title": "Summer of Love",
            "transliterated_title": "Summer of Love",
            "publication_year": "2020",
            "pagination": None,
            "edition": None,
            "publisher_name": "Project Gutenberg",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Kilmer, Joyce",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "False",
            "gold_rush": "summeroflove__________________________________________________________2020_______projea_______________________________________________________kilme_______________p",
        },
        "tests/fixtures/alma_marc_records_short.csv7": {
            "id": "99125448317806421",
            "title": "Verses",
            "transliterated_title": "Verses",
            "publication_year": "2019",
            "pagination": None,
            "edition": None,
            "publisher_name": "Project Gutenberg",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Belloc, Hilaire",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "False",
            "gold_rush": "verses________________________________________________________________2019_______projea_______________________________________________________bello_______________p",
        },
        "tests/fixtures/alma_marc_records_short.csv8": {
            "id": "99125411062906421",
            "title": "North Carolina : land of water, land of sky",
            "transliterated_title": "North Carolina : land of water, land of sky",
            "publication_year": "2021",
            "pagination": "ix 225 pages",
            "edition": None,
            "publisher_name": "The University of North Carolina Press",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Simpson, Bland",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "False",
            "gold_rush": "northcarolinalandofwaterlandofsky_____________________________________2021225____theuna_______________________________________________________simps_______________p",
        },
        "tests/fixtures/alma_marc_records_short.csv9": {
            "id": "99125358230606421",
            "title": "Science communication : a practical guide for scientists",
            "transliterated_title": "Science communication : a practical guide for scientists",
            "publication_year": "2013",
            "pagination": "1 online resource 402 pages",
            "edition": None,
            "publisher_name": "Wiley",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": None,
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "sciencecommunicationapracticalguideforscientists______________________20131______wileya___________________________________________________________________________e",
        },
        "tests/fixtures/alma_marc_records_short.csv10": {
            "id": "99125358072606421",
            "title": "Science : a many-splendored thing",
            "transliterated_title": "Science : a many-splendored thing",
            "publication_year": "2011",
            "pagination": "1 online resource 337 pages",
            "edition": "1st edition",
            "publisher_name": "World Scientific",
            "type_of": "a",
            "title_part": None,
            "title_number": None,
            "author": "Novak, Igor",
            "title_inclusive_dates": None,
            "gov_doc_number": None,
            "is_electronic_resource": "True",
            "gold_rush": "scienceamanysplendoredthing___________________________________________20111___1__worlda_______________________________________________________novak_______________e",
        },
    }


# pylint: enable=line-too-long


@pytest.fixture(name="console_inputs")
def fixture_console_inputs():
    return [
        "n",
        "y",
        "n",
        "n",
        "y",
        "y",
        "n",
        "n",
        "y",
        "y",
        "y",
        "y",
        "y",
        "y",
        "y",
        "f",
    ]


# pylint: disable=too-few-public-methods
class Helpers:
    @staticmethod
    def file_cleanup(files):
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass


# pylint: enable=too-few-public-methods


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture(name="all_files")
def fixture_all_files():
    return [
        "tests/test_outputs/data_matching_learned_settings",
        "tests/test_outputs/data_matching_output.csv",
        "tests/test_outputs/data_matching_training.json",
    ]
