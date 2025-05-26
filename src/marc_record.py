import string
import re
import pymarc
from src.gold_rush import GoldRush


class MarcRecord:
    def __init__(self, record):
        self.record = record

    def to_dictionary(self):
        """Takes a MarcRecord and returns a dictionary including the most salient fields"""
        return {
            "id": self.id(),
            "title": self.title(),
            "transliterated_title": self.transliterated_title(),
            "publication_year": self.publication_year() or "",
            "pagination": self.pagination(),
            "edition": self.edition(),
            "publisher_name": self.publisher_name(),
            "type_of": self.type_of(),
            "title_part": self.title_part(),
            "title_number": self.title_number(),
            "author": self.author(),
            "title_inclusive_dates": self.title_inclusive_dates(),
            "gov_doc_number": self.gov_doc_number(),
            "is_electronic_resource": self.is_electronic_resource(),
            "gold_rush": GoldRush(self).as_gold_rush(),
        }

    def id(self):
        try:
            return self.record.get("001").data
        except (KeyError, AttributeError):
            return ""

    def title(self):
        if self.__vernacular_title_field():
            title_field = self.__vernacular_title_field()
        else:
            title_field = self.__title_from_245()
        try:
            subfield_a = str(title_field.get("a") or "")
            subfield_b = str(title_field.get("b") or "")
            subfield_p = str(title_field.get("p") or "")
            title = " ".join([subfield_a, subfield_b, subfield_p])
            title = self.__strip_ending_punctuation(title)
            return title
        except (KeyError, AttributeError):
            return ""

    def transliterated_title(self):
        title_field = self.__title_from_245()
        try:
            subfield_a = str(title_field.get("a") or "")
            subfield_b = str(title_field.get("b") or "")
            subfield_p = str(title_field.get("p") or "")
            title = " ".join([subfield_a, subfield_b, subfield_p])
            title = self.__strip_ending_punctuation(title)
            return title
        except (KeyError, AttributeError):
            return ""

    def __title_from_245(self):
        try:
            title = self.record["245"]
            return title
        except KeyError:
            return ""

    def __vernacular_title_field(self):
        try:
            return self.record.get_linked_fields(self.record["245"])[0]
        except (KeyError, IndexError, pymarc.exceptions.MissingLinkedFields):
            return ""

    def publication_year(self):
        pub_year = None
        if self.date_one() and self.date_two():
            pub_year = self.date_two()
        elif self.date_one() and not self.date_two():
            pub_year = self.date_one()
        elif (
            not self.date_one() and not self.date_two() and self.__date_of_production()
        ):
            pub_year = self.__date_of_production()
        elif (
            not self.date_one()
            and not self.date_two()
            and not self.__date_of_production()
            and self.__date_of_publication()
        ):
            pub_year = self.__date_of_publication()
        return pub_year

    def pagination(self):
        try:
            subfield_a = self.record["300"].get("a")
            if subfield_a:
                return self.__normalize_extent(subfield_a)
            return ""
        except KeyError:
            return ""

    def edition(self):
        try:
            return self.__normalize_edition(self.record["250"].get("a"))
        except KeyError:
            return ""

    def publisher_name(self):
        try:
            pub = self.record["264"]["b"]
        except KeyError:
            try:
                pub = self.record["260"]["b"]
            except KeyError:
                return ""
        return self.__strip_punctuation(pub)

    def type_of(self):
        return self.record.leader.type_of_record

    def title_part(self):
        try:
            parts = self.record["245"].get_subfields("p")[1:]
            return self.__strip_punctuation(" ".join(parts))
        except KeyError:
            return ""

    def title_number(self):
        try:
            num = self.record["245"].get("n")
            if num:
                return self.__strip_punctuation(num)
            return ""
        except KeyError:
            return ""

    def author(self):
        if self.__vernacular_author_field():
            author_field = self.__vernacular_author_field()
        else:
            author_field = self.__author_from_1xx()

        if author_field:
            try:
                return self.__strip_ending_punctuation(author_field.get("a"))
            except AttributeError:
                return ""
        return ""

    def __author_from_1xx(self):
        try:
            return self.record["100"]
        except KeyError:
            try:
                return self.record["110"]
            except KeyError:
                try:
                    return self.record["111"]
                except KeyError:
                    return ""

    def __vernacular_author_field(self):
        try:
            return self.record.get_linked_fields(self.record["100"])[0]
        except (KeyError, IndexError, pymarc.exceptions.MissingLinkedFields):
            try:
                return self.record.get_linked_fields(self.record["110"])[0]
            except (KeyError, IndexError, pymarc.exceptions.MissingLinkedFields):
                try:
                    return self.record.get_linked_fields(self.record["111"])[0]
                except (KeyError, IndexError, pymarc.exceptions.MissingLinkedFields):
                    return ""

    def title_inclusive_dates(self):
        try:
            date = self.record["245"].get("f")
            if date:
                return self.__strip_ending_punctuation(date)
            return ""
        except KeyError:
            return ""

    def gov_doc_number(self):
        try:
            return self.record["086"].get("a")
        except KeyError:
            return ""

    def is_electronic_resource(self):
        return bool(
            self.__is_electronic_resource_from_title()
            or self.__is_electronic_resource_from_reproduction()
            or self.__is_electronic_resource_from_description()
            or self.__is_electronic_resource_from_007()
        )

    def __is_electronic_resource_from_title(self):
        try:
            return self.record["245"].get("h") == "[electronic resource]"
        except KeyError:
            return False

    def __is_electronic_resource_from_reproduction(self):
        try:
            return re.match(
                "electronic reproduction", self.record["533"].get("a"), re.IGNORECASE
            )
        except (KeyError, TypeError):
            return False

    def __is_electronic_resource_from_description(self):
        try:
            subfield_a = self.record["300"].get("a")
            if subfield_a:
                return bool(re.search("online resource", subfield_a, re.IGNORECASE))
            return False
        except KeyError:
            return False

    def __is_electronic_resource_from_007(self):
        try:
            return bool(self.record["007"].data[0] == "c")
        except KeyError:
            return False

    def __normalize_edition(self, edition):
        edition_mapping = {r"Ed\.": "Edition", r"ed\.": "edition"}
        try:
            for key, value in edition_mapping.items():
                edition = re.sub(key, value, edition)
            return self.__strip_punctuation(edition)
        except TypeError:
            return ""

    def __normalize_extent(self, extent):
        extent_mapping = {
            r"p\.": "pages",
            r"v\.": "volumes",
            r"vol\.": "volumes",
            r"ℓ\.": "leaves",
        }
        for key, value in extent_mapping.items():
            extent = re.sub(key, value, extent)
        return self.__strip_punctuation(extent)

    def __strip_ending_punctuation(self, some_string):
        punctuation_to_strip = string.punctuation.replace(")", "")
        return some_string.strip(punctuation_to_strip + " ")

    def __strip_punctuation(self, some_string):
        punctuation_to_strip = string.punctuation.replace("&", "")
        some_string = some_string.translate(str.maketrans("", "", punctuation_to_strip))
        some_string = re.sub("  ", " ", some_string).strip()
        return some_string

    def is_valid_date(self, date_string):
        valid = True
        if date_string == "9999":
            valid = False
        elif date_string == "    ":
            valid = False
        elif self.number_of_characters(date_string) != 4:
            valid = False
        try:
            int(date_string)
        except (ValueError, TypeError):
            valid = False
        return valid

    def number_of_characters(self, date_string):
        try:
            return len(date_string)
        except TypeError:
            return False

    def date_one(self):
        try:
            date_string = self.record["008"].data[7:11]
            return self.__as_date(date_string)
        except KeyError:
            return None

    def date_two(self):
        try:
            date_string = self.record["008"].data[11:15]
            return self.__as_date(date_string)
        except KeyError:
            return None

    def __date_of_production(self):
        try:
            date_string = self.record["264"]["c"]
        except KeyError:
            return None
        return self.__as_date(date_string)

    def __date_of_publication(self):
        try:
            date_string = self.record["260"]["c"]
        except KeyError:
            return ""
        return self.__as_date(date_string)

    def __as_date(self, date_string):
        # Remove punctuation (for 260 and 264 fields)
        date_string = self.__strip_punctuation(date_string)
        if self.is_valid_date(date_string):
            return int(date_string)
        return ""
