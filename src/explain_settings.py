import dedupe
import os

settings_file = "data_matching_learned_settings"

if os.path.exists(settings_file):
    print("reading from", settings_file)
    with open(settings_file, "rb") as sf:
        linker = dedupe.StaticRecordLink(sf)

linker_dict = linker.__dict__
linker_dict.update(_fingerprinter=linker._fingerprinter.__dict__)

linker_dict.update(data_model=linker.data_model.__dict__)

print(linker_dict)
