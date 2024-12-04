import pytest
from pymarc import parse_xml_to_array, Record, Field, Subfield, Leader
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush

records = parse_xml_to_array('alma_marc_records.xml')
record_from_file = records[0]

def test_potentially_empty_fields():
  for record in records:
    new_record = MarcRecord(record)
    new_record.to_dictionary()
    new_record.as_gold_rush()

def test_title():
  pymarc_record = Record()
  pymarc_record.add_field(
    Field(tag='245', subfields=[Subfield(code='a', value='Short title')])
  )
  new_record = MarcRecord(pymarc_record)
  new_string = GoldRush(new_record)
  assert(new_string.title()) == 'Short_title___________________________________________________________'

