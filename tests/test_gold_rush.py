import pytest
from pymarc import parse_xml_to_array, Record, Field, Subfield, Leader
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush

records = parse_xml_to_array('alma_marc_records.xml')
record_from_file = records[0]

def test_potentially_empty_fields():
  for record in records:
    new_record = MarcRecord(record)
    new_string = GoldRush(new_record)
    new_string.as_gold_rush()

def test_as_gold_rush():
  pymarc_record = record_from_file
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.as_gold_rush()) == 'science_a_poem_dedicated_to_the_american_association_for_the_advanceme18561___'

def test_title():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='245', subfields=[Subfield(code='a', value='Short title')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.title()) == 'short_title___________________________________________________________'

def test_long_title():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='245', subfields=[Subfield(code='a', value='Science :'), Subfield(code='b', value='a poem dedicated etc. : and so forth /'),
                                Subfield(code='p', value='Labor unions'), Subfield(code='p', value='Supplement')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.title()) == 'science_a_poem_dedicated_etc_and_so_forth_labor_unions________________'

def test_pagination():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='300', subfields=[Subfield(code='a', value='578 p. ; '), Subfield(code='c', value='27 cm')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.pagination()) == '578_'

def test_pagination_record():
  pymarc_record = record_from_file
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.pagination()) == '1___'

def test_edition_as_gold_rush():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='250', subfields=[Subfield(code='a', value='2nd Ed.')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.edition()) == '2__'

def test_edition_as_gold_rush_alpha():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='250', subfields=[Subfield(code='a', value='First edition')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.edition()) == 'fir'

def test_empty_edition_as_gold_rush():
  pymarc_record = Record()
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.edition()) == '___'
