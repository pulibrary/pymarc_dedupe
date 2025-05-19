import csv
import io
import itertools


# pylint: disable=too-few-public-methods
class Readable:
    def __init__(self, iterator):
        self.output = io.StringIO()
        self.writer = csv.writer(self.output)
        self.iterator = iterator

    def read(self, size):
        self.writer.writerows(itertools.islice(self.iterator, size))

        chunk = self.output.getvalue()
        self.output.seek(0)
        self.output.truncate(0)

        return chunk


# pylint: enable=too-few-public-methods
