import string
import re

class GoldRush:
  def __init__(self, marc_record):
    self.marc_record = marc_record

  def title(self):
    some_string = self.marc_record.title().translate(str.maketrans(' ', '_'))
    some_string = some_string.ljust(70, '_')
    return some_string[0:70]

  