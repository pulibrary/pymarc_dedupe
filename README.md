The purpose of this code is to provide consistent Marc record parsing for deduplication, in order to compare how humans, a machine learning deduplication algorithm, and an implementation of the GoldRush algorithm deduplicate Marc records.

The intention is that the output of the current MarcRecord methods be human-readable and used for the machine learning deduplication algorithm, and the GoldRush methods be used to build a string for literal matching. 

The implementation of the GoldRush algorithm is based on the [Colorado Alliance MARC record match key generation](https://coalliance.org/sites/default/files/GoldRush-Match_KeyJanuary2024_0.doc), documented January 12, 2024.


## Developing this application
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
pip install -r requirements.txt
```

## Testing
1. Install pytest
```bash
pip install -U pytest
```

