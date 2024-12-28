import string
import re


class MarcRecord:
    def __init__(self, record):
        self.record = record

    def to_dictionary(self):
        """Takes a MarcRecord and returns a dictionary including the most salient fields"""
        return {
            "title": self.title(),
            "publication_year": self.publication_year(),
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
        }

    def title(self):
        if self.vernacular_title_field():
            title_field = self.vernacular_title_field()
        else:
            title_field = self.title_from_245()
        try:
            subfield_a = str(title_field.get("a") or "")
            subfield_b = str(title_field.get("b") or "")
            subfield_p = str(title_field.get("p") or "")
            title = " ".join([subfield_a, subfield_b, subfield_p])
            title = self.strip_ending_punctuation(title)
            return title
        except (KeyError, AttributeError):
            return None

    def title_from_245(self):
        try:
            title = self.record["245"]
            return title
        except KeyError:
            return None

    def vernacular_title_field(self):
        try:
            return self.record.get_linked_fields(self.record["245"])[0]
        except (KeyError, IndexError):
            return None

    def publication_year(self):
        pub_year = ""
        if self.date_one() and self.date_two():
            pub_year = self.date_two()
        elif self.date_one() and not self.date_two():
            pub_year = self.date_one()
        elif not self.date_one() and not self.date_two() and self.date_of_production():
            pub_year = self.date_of_production()
        elif (
            not self.date_one()
            and not self.date_two()
            and not self.date_of_production()
            and self.date_of_publication()
        ):
            pub_year = self.date_of_publication()
        return pub_year

    def pagination(self):
        try:
            return self.normalize_extent(self.record["300"].get("a"))
        except KeyError:
            return None

    def edition(self):
        try:
            return self.normalize_edition(self.record["250"].get("a"))
        except KeyError:
            return None

    def publisher_name(self):
        try:
            pub = self.record["264"]["b"]
        except KeyError:
            try:
                pub = self.record["260"]["b"]
            except KeyError:
                return None
        return self.strip_punctuation(pub)

    def type_of(self):
        return self.record.leader.type_of_record

    def title_part(self):
        parts = self.record["245"].get_subfields("p")[1:]
        return self.strip_punctuation(" ".join(parts))

    def title_number(self):
        num = self.record["245"].get("n")
        if num:
            return self.strip_punctuation(num)
        return None

    def author(self):
        if self.vernacular_author_field():
            author_field = self.vernacular_author_field()
        else:
            author_field = self.author_from_1xx()

        if author_field:
            return self.strip_ending_punctuation(author_field.get("a"))
        return None

    def author_from_1xx(self):
        try:
            return self.record["100"]
        except KeyError:
            try:
                return self.record["110"]
            except KeyError:
                try:
                    return self.record["111"]
                except KeyError:
                    return None

    def vernacular_author_field(self):
        try:
            return self.record.get_linked_fields(self.record["100"])[0]
        except (KeyError, IndexError):
            try:
                return self.record.get_linked_fields(self.record["110"])[0]
            except (KeyError, IndexError):
                try:
                    return self.record.get_linked_fields(self.record["111"])[0]
                except (KeyError, IndexError):
                    return None

    def title_inclusive_dates(self):
        date = self.record["245"].get("f")
        if date:
            return self.strip_punctuation(date)
        return None

    def gov_doc_number(self):
        try:
            return self.record["086"].get("a")
        except KeyError:
            return None

    def is_electronic_resource(self):
        return bool(
            self.is_electronic_resource_from_title()
            or self.is_electronic_resource_from_reproduction()
            or self.is_electronic_resource_from_description()
            or self.is_electronic_resource_from_007()
        )

    def is_electronic_resource_from_title(self):
        try:
            return self.record["245"].get("h") == "[electronic resource]"
        except KeyError:
            return False

    def is_electronic_resource_from_reproduction(self):
        try:
            return re.match(
                "electronic reproduction", self.record["533"].get("a"), re.IGNORECASE
            )
        except KeyError:
            return False

    def is_electronic_resource_from_description(self):
        try:
            return bool(re.search("online resource", self.record["300"].get("a"), re.IGNORECASE))
        except KeyError:
            return False

    def is_electronic_resource_from_007(self):
        try:
            return bool(self.record["007"].data[0] == "c")
        except KeyError:
            return False

    def normalize_edition(self, edition):
        edition_mapping = {"Ed.": "Edition", "ed.": "edition"}
        for key, value in edition_mapping.items():
            edition = re.sub(key, value, edition)
        return self.strip_punctuation(edition)

    def normalize_extent(self, extent):
        extent_mapping = {
            r"p\.": "pages",
            r"v\.": "volumes",
            r"vol\.": "volumes",
            r"ℓ\.": "leaves",
        }
        for key, value in extent_mapping.items():
            extent = re.sub(key, value, extent)
        return self.strip_punctuation(extent)

    def strip_ending_punctuation(self, some_string):
        punctuation_to_strip = string.punctuation.replace(")", "")
        return some_string.strip(punctuation_to_strip + " ")

    def strip_punctuation(self, some_string):
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
        date_string = self.record["008"].data[7:11]
        return self.as_date(date_string)

    def date_two(self):
        date_string = self.record["008"].data[11:15]
        return self.as_date(date_string)

    def date_of_production(self):
        try:
            date_string = self.record["264"]["c"]
        except KeyError:
            return None
        return self.as_date(date_string)

    def date_of_publication(self):
        try:
            date_string = self.record["260"]["c"]
        except KeyError:
            return None
        return self.as_date(date_string)

    def as_date(self, date_string):
        # Remove punctuation (for 260 and 264 fields)
        date_string = self.strip_punctuation(date_string)
        if self.is_valid_date(date_string):
            return int(date_string)
        return None
