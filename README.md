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
1. Set up the environment, as described below
2. Call the main.py python script with arguments for the file or files you want to compare.

   You can give either MarcXML or JSON files, and either one file (will find duplicates within that files) or two files (will find duplicates within and between the files) - file1 is required, file2 and dir are not required.

Compare two MarcXML files
```bash
python main.py --file1="tests/fixtures/alma_marc_records_short.xml" --file2="tests/fixtures/alma_marc_records.xml" --dir="experiments_files_and_output"
```
Find duplicates in a single JSON file
```bash
python main.py --file1="tests/fixtures/marc_records.json"
```
3. If you do not already have settings and training data, it will open an interactive session in your terminal to see whether you, as a human, think two things are duplicates or not, to train the Machine Learning algorithm. Follow the instructions in your terminal
4. It will output a CSV of all the records you input, with three added columns:
  a. Cluster ID - all records that it thinks are matches of each other will have the same Cluster ID. If a record does not have a Cluster ID, that means the machine learning algorithm does not think it has any duplicates.
  b. Link score - how confident the algorithm is that the record belongs to its cluster. The higher the number, the more likely the record is a true match
  c. source file - which file the record displayed is from

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
pip install -r requirements/[environment].txt

pip install -r requirements/development.txt

OR

pip install -r requirements/common.txt
```

Bring up the database using lando

```bash
lando start
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
pylint src tests main.py --disable=C0114,C0115,C0116
```
