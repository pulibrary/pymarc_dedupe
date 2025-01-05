[![CircleCI](https://dl.circleci.com/status-badge/img/gh/pulibrary/pymarc_dedupe/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/pulibrary/pymarc_dedupe/tree/main)
[![Coverage Status](https://coveralls.io/repos/github/pulibrary/pymarc_dedupe/badge.svg?branch=main)](https://coveralls.io/github/pulibrary/pymarc_dedupe?branch=main)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pulibrary/pymarc_dedupe)


The purpose of this code is to provide consistent Marc record parsing for deduplication, in order to compare how humans, a machine learning deduplication algorithm, and an implementation of the GoldRush algorithm deduplicate Marc records.

The intention is that the output of the current MarcRecord methods be human-readable and used for the machine learning deduplication algorithm, and the GoldRush methods be used to build a string for literal matching. 

The implementation of the GoldRush algorithm is based on the [Colorado Alliance MARC record match key generation](https://coalliance.org/sites/default/files/GoldRush-Match_KeyJanuary2024_0.doc), documented January 12, 2024.

## Decisions
This application will provide two layers of normalization.

### First layer of normalization - humans and machine learning algorithm
The first layer of normalization consists of selecting a subset of Marc fields and subfields for human and machine learning algorithm comparison.

This will include showing fields in the vernacular script when available. Since not everyone is familiar with different scripts, these will be presented with both the transliterated information and the vernacular script. The vernacular script is more likely to be accurately matched by both the machine learning algorithm and humans who are familiar with that script, the transliterated script is more likely to be accurately matched by humans who are not familiar with the vernacular script.

### Second layer of normalization - GoldRush algorithm
The second layer of normalization will be built on the first layer of normalization, and will be an interpretation of the GoldRush algorithm, intended for exact string matching. 

To this end, there will be much more strict string normalization in this layer. Only vernacular versions of fields will be preserved.

- Some normalization strongly favors English-language texts - e.g.
  - Replacing English-language articles at the beginnings of titles
    - This also seems like it duplicates the 245 second indicator for non-filing characters
  - Replacing '&' with 'and'

## Using the code
This obviously needs to be refined

1. Start python interactive interpreter
```bash
python
```
2. Import needed libraries
```python
from pymarc import parse_xml_to_array
from src.marc_record import MarcRecord
from src.gold_rush import GoldRush
```
3. Create an object with example marc records from marc xml
```python
all_records = parse_xml_to_array("alma_marc_records.xml")
```
4. Create a dictionary of an example record
```python
new_record = MarcRecord(all_records[0])
new_record.to_dictionary()
```
5. Create a GoldRush string of an example record
```python
gr = GoldRush(new_record)
gr.as_gold_rush()
```

6. create list of GoldRush strings
```python
list_of_records = []
for record in all_records:
  mr = MarcRecord(record)
  gr = GoldRush(mr)
  list_of_records.append(gr.as_gold_rush())
```

## Developing this application
### Set-up and install dependencies
1. Make a .venv
```
python3 -m venv .venv
```
2. activate the environment
```bash
. .venv/bin/activate
```

3. install dependencies
```bash
pip install -r requirements/development.txt
```

### Testing
```bash
pytest
```

### Linting
1. ruff - fast
  - Formatter - `--check` flag does not make changes. Run without `--check` flag for automatic fixing
  ```bash
  ruff format . --check
  ```
  - Linter
  ```bash
  ruff check .
  ```
2. pylint - slower, does more in-depth checks
  - Currently excluding checks for documentation - remove these disables once this is remediated
```bash
pylint src tests --disable=C0114,C0115,C0116
```
