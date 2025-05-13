import re
from unidecode import unidecode


class GoldRush:
    def __init__(self, marc_record):
        self.marc_record = marc_record

    def as_gold_rush(self):
        return (
            self.title()
            + (self.publication_year() or '')
            + self.pagination()
            + self.edition()
            + self.publisher_name()
            + self.marc_record.type_of()
            + self.title_part()
            + self.title_number()
            + self.title_inclusive_dates()
            + self.author()
            + self.gov_doc_number()
            + self.format_character()
        )

    def title(self):
        some_string = self.normalize_title(self.marc_record.title())
        return self.pad(some_string, 70)

    def title_part(self):
        some_string = self.normalize_title(self.marc_record.title_part())
        return self.pad(some_string, 30)

    def publication_year(self):
        some_string = str(self.marc_record.publication_year() or '')
        return self.pad(some_string, 4)

    def pagination(self):
        try:
            nums = re.findall(r"\d+", self.marc_record.pagination())[0]
        except (TypeError, IndexError):
            nums = ""
        return self.pad(nums, 4)

    def edition(self):
        lowercase_ed = ""
        try:
            lowercase_ed = self.marc_record.edition().lower()
            chars = re.findall(r"\d+", lowercase_ed)[0]
        except (TypeError, IndexError):
            try:
                chars = re.findall(r"\w+", lowercase_ed)[0]
                chars = chars[0:3]
                for ordinal, numeral in self.edition_dictionary().items():
                    chars = chars.replace(ordinal, numeral)
            except (TypeError, IndexError):
                chars = ""
        return unidecode(self.pad(chars, 3))

    def publisher_name(self):
        publisher_name = self.marc_record.publisher_name().lower()
        publisher_name = publisher_name.translate(
            str.maketrans(self.title_translation_dictionary())
        )
        return self.pad(publisher_name, 5)

    def title_number(self):
        title_number = self.marc_record.title_number() or ""
        return self.pad(title_number, 10)

    def title_inclusive_dates(self):
        title_dates = self.marc_record.title_inclusive_dates() or ""
        title_dates = self.strip_punctuation(title_dates)
        return self.pad(title_dates, 15)

    def author(self):
        author = self.marc_record.author() or ""
        author = self.strip_punctuation(author)
        return self.pad(author, 5)

    def gov_doc_number(self):
        gov_doc_number = self.marc_record.gov_doc_number() or ""
        gov_doc_number = self.strip_punctuation(gov_doc_number)
        return self.pad(gov_doc_number, 15)

    def format_character(self):
        if self.marc_record.is_electronic_resource():
            return "e"
        return "p"

    def edition_dictionary(self):
        return {
            "fir": "1__",
            "sec": "2__",
            "thr": "3__",
            "fou": "4__",
            "fiv": "5__",
            "six": "6__",
            "sev": "7__",
            "eig": "8__",
            "nin": "9__",
            "ten": "10_",
        }

    def normalize_title(self, some_string):
        some_string = some_string.strip().lower()
        # remove beginning English articles
        some_string = re.sub("^the +", "", some_string)
        some_string = re.sub("^a +", "", some_string)
        some_string = re.sub("^an +", "", some_string)
        some_string = some_string.translate(
            str.maketrans(self.title_translation_dictionary())
        )
        return unidecode(some_string)

    def title_translation_dictionary(self):
        return {
            "&": "and",
            "%": "",
            "'": "",
            "{": "",
            "}": "",
            " ": "",
            "!": "",
            '"': "",
            "#": "",
            "$": "",
            "(": "",
            ")": "",
            "*": "",
            "+": "",
            ",": "",
            "-": "",
            ".": "",
            "/": "",
            ":": "",
            ";": "",
            "<": "",
            "=": "",
            ">": "",
            "?": "",
            "@": "",
            "[": "",
            "\\": "",
            "]": "",
            "^": "",
            "`": "",
            "|": "",
            "~": "",
            "©": "",
        }

    def pad(self, string, length):
        return string.ljust(length, "_")[0:length]

    def strip_punctuation(self, some_string):
        some_string = re.sub("  ", " ", some_string).strip().lower()
        some_string = re.sub("^the +", "", some_string)
        some_string = some_string.translate(
            str.maketrans(self.translation_dictionary())
        )
        return unidecode(some_string)

    def translation_dictionary(self):
        return {
            "&": "and",
            "%": "_",
            "'": "",
            "{": "",
            "}": "",
            " ": "_",
            "!": "_",
            '"': "_",
            "#": "_",
            "$": "_",
            "(": "_",
            ")": "_",
            "*": "_",
            "+": "_",
            ",": "_",
            "-": "_",
            ".": "_",
            "/": "_",
            ":": "_",
            ";": "_",
            "<": "_",
            "=": "_",
            ">": "_",
            "?": "_",
            "@": "_",
            "[": "_",
            "\\": "_",
            "]": "_",
            "^": "_",
            "`": "_",
            "|": "_",
            "~": "_",
            "©": "_",
        }
