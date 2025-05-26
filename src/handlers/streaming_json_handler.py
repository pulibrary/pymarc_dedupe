import ijson
from pymarc import JSONHandler


def parse_json(json_file, handler):
    with open(json_file, "rb") as file:
        parser = ijson.items(file, "item")
        for item in parser:
            handler.element(item)


def map_json(function, *files):
    """Map a function onto the file.

    So that for each record that is parsed the function will get called with the
    extracted record

    .. code-block:: python

        def do_it(r):
            print(r)

        map_json(do_it, 'marc.json')
    """
    handler = JSONHandler()
    # this overrides the #process_record function in the JSONHandler class in pymarc
    handler.process_record = function
    for json_file in files:
        parse_json(json_file, handler)
