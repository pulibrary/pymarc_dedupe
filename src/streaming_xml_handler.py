import unicodedata
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from pymarc import Leader, XmlHandler, exceptions

MARC_XML_NS = "http://www.loc.gov/MARC21/slim"


class StreamingXmlHandler(XmlHandler):
    def endElementNS(self, name, qname):
        """End element NS."""
        if self._strict and name[0] != MARC_XML_NS:
            return

        element = name[1]
        if self.normalize_form is not None:
            text = unicodedata.normalize(self.normalize_form, "".join(self._text))
        else:
            text = "".join(self._text)
        try:
            if element == "record":
                self.process_record(self._record)
                self._record = None
            elif element == "leader":
                self._record.leader = Leader(text)
            elif element == "controlfield":
                self._field.data = text
                self._record.add_field(self._field)
                self._field = None
            elif element == "datafield":
                self._record.add_field(self._field)
                self._field = None
            elif element == "subfield":
                self._field.add_subfield(self._subfield_code, text)
                self._subfield_code = None
        except exceptions.RecordLeaderInvalid:
            pass

        self._text = []


def map_xml(function, *files):
    """Map a function onto the file.

    So that for each record that is parsed the function will get called with the
    extracted record

    .. code-block:: python

        def do_it(r):
            print(r)

        map_xml(do_it, 'marc.xml')
    """
    handler = StreamingXmlHandler()
    handler.process_record = function
    for xml_file in files:
        parse_xml(xml_file, handler)


def parse_xml(xml_file, handler):
    """Parse a file with a given subclass of xml.sax.handler.ContentHandler."""
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setFeature(feature_namespaces, 1)
    parser.parse(xml_file)
