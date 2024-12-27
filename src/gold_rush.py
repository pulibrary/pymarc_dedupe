import string
import re

class GoldRush:
  def __init__(self, marc_record):
    self.marc_record = marc_record

  def as_gold_rush(self):
    return self.title() + self.publication_year() + self.pagination()

  def title(self):
    some_string = self.strip_punctuation(self.marc_record.title())
    some_string = some_string.ljust(70, '_')
    return some_string[0:70]

  def publication_year(self):
    return str(self.marc_record.publication_year() or '')

  def pagination(self):
    try:
      nums =  re.findall(r'\d+', self.marc_record.pagination())[0]
      return nums.ljust(4, '_')[0:4]
    except (TypeError, IndexError):
      return '____'

  def edition(self):
    lowercase_ed = ''
    try:
      lowercase_ed = self.marc_record.edition().lower()
      chars =  re.findall(r'\d+', lowercase_ed)[0]
    except (TypeError, IndexError, AttributeError):
      try:
        chars =  re.findall(r'\w+', lowercase_ed)[0]
      except (TypeError, IndexError, AttributeError):
        return '___'
    return chars.ljust(3, '_')[0:3]

  def strip_punctuation(self, some_string):
    some_string = re.sub('  ', ' ', some_string).strip().lower()
    some_string = re.sub('^the +', '', some_string)
    some_string = some_string.translate(str.maketrans(self.translation_dictionary()))
    
    return some_string

  def translation_dictionary(self):
    dict = {
      '&': 'and',
      '%': '_',
      "'": '',
      '{': '',
      '}': '',
      ' ': '_',
      '!': '_',
      '"': '_',
      '#': '_',
      '$': '_',
      '(': '_',
      ')': '_',
      '*': '_',
      '+': '_',
      ',': '_',
      '-': '_',
      '.': '_',
      '/': '_',
      ':': '_',
      ';': '_',
      '<': '_',
      '=': '_',
      '>': '_',
      '?': '_',
      '@': '_',
      '[': '_',
      "\\": '_',
      ']': '_',
      '^': '_',
      '`': '_',
      '|': '_',
      '~': '_',
      '©': '_'

    }
    return dict
