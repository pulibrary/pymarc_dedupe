import pytest
from src.parse_marc_xml import ParseMarcXML
def test_publication_year():
    # If date_two is blank, use date_one
    assert(ParseMarcXML.publication_year('1984','    ','1999',None)) == '1984'
    # If date_two is 9999, use date_one
    assert(ParseMarcXML.publication_year('1984','9999',None, None)) == '1984'
    # If date_two does not have 4 digits, use date_one
    assert(ParseMarcXML.publication_year('1984','20006','1999',None)) == '1984'
    # If both date_one and date_two are valid dates, use date_two
    assert(ParseMarcXML.publication_year('1984','2006','1999',None)) == '2006'
    # If neither date_one nor date_two are valid dates, use date from 264$c
    assert(ParseMarcXML.publication_year('198','200','1999',None)) == '1999'
    # If neither date_one nor date_two are valid dates, and 264 $c is also not a valid date, use date from 260 $c
    assert(ParseMarcXML.publication_year('198','200','199', '1885')) == '1885'
    # If a valid number is not found, return '0000'
    assert(ParseMarcXML.publication_year('198','200','199',None)) == '0000'

def test_valid_date():
    assert(ParseMarcXML.valid_date('9999')) == False
    assert(ParseMarcXML.valid_date('    ')) == False
    assert(ParseMarcXML.valid_date('123')) == False
    assert(ParseMarcXML.valid_date('abcd')) == False
    assert(ParseMarcXML.valid_date(None)) == False

