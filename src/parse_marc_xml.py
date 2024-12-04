from pymarc import parse_xml_to_array

class ParseMarcXML:
  records = parse_xml_to_array('alma_marc_records.xml')
  record = records[0]

  def title(title_field):
    return ' '.join(title_field.get_subfields('a', 'b', 'p'))

  def publication_year(date_one, date_two, date_of_production, date_of_publication):
    pub_year = ''
    if ParseMarcXML.valid_date(date_one) and ParseMarcXML.valid_date(date_two):
      pub_year = date_two
    elif ParseMarcXML.valid_date(date_one) and not ParseMarcXML.valid_date(date_two):
      pub_year = date_one
    elif not ParseMarcXML.valid_date(date_one) and not ParseMarcXML.valid_date(date_two) and ParseMarcXML.valid_date(date_of_production):
      pub_year = date_of_production
    elif not ParseMarcXML.valid_date(date_one) and not ParseMarcXML.valid_date(date_two) and not ParseMarcXML.valid_date(date_of_production) and ParseMarcXML.valid_date(date_of_publication):
      pub_year = date_of_publication
    else:
      pub_year = '0000'

    return pub_year

  def date_of_production(record):
    try:
      return record['264']['c']
    except KeyError:
      return None
    
  def date_of_publication(record):
    try:
      return record['260']['c']
    except KeyError:
      return None

  def valid_date(date_string):
    valid = True
    if date_string == '9999':
      valid = False
    elif date_string == '    ':
      valid = False
    elif ParseMarcXML.number_of_characters(date_string) != 4:
      valid = False
    try:
      int(date_string)
    except (ValueError, TypeError):
      valid = False
    return valid

  def number_of_characters(date_string):
    try:
      return len(date_string)
    except TypeError:
      return False


  title = title(record['245'])

  control_data = record['008'].data
  date_one = control_data[7:11]
  date_two = control_data[11:15]
  date_of_production = date_of_production(record)
  date_of_publication = date_of_publication(record)
  print(date_of_publication)
  # pub_year = publication_year(date_one, date_two, date_of_production, date_of_publication)

