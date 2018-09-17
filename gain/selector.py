import re
import logging as logger

from lxml import etree
import lxml.html as lx
from pyquery import PyQuery as pq
from .tool import Manipulation

manipulation_options = [
    "clean_string",
    "extract_email",
    "extract_phone",
    "extract_website",
    "to_date_iso"
]

class Selector:
    def __init__(self, rule, attr=None, **kwargs):
        self.rule = rule
        self.attr = attr
        self.index = 0
        self.manipulate = []
        self.page_element , self.method = (None,)*2

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def parse_detail(self, html, **options):
        raise NotImplementedError

# Deprecated original Css code.
class Pyq(Selector):
    def parse_detail(self, html):
        d = pq(html)
        if self.attr is None:
            try:
                return d(self.rule)[0].text
            except IndexError:
                return None
        return d(self.rule)[0].attr(self.attr, None)


class Css(Selector):
 
    def _set_element(self, fn):
            try:
                self.page_element = fn()
            except (Exception, IndexError) as e:
                self.page_element = None
                logger.error( 'Error:{0}'.format(e))

    def parse_detail(self, html):
        """
            DOCS: 21.5.3.2. Element Objects
            https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.attrib
        """
        self.doc = lx.fromstring(html)
        self.css_select = self.doc.cssselect
        self.xpath = self.doc.xpath

        # This makes it backwards compatible to V0.1.14 for original "rule" unless JQuery statements have been used
        if not self.method and self.attr is None:  
            self._set_element(
                lambda: self.css_select(self.rule)[0].text
                )

        elif self.method == 'text':
            self._set_element(
                lambda: self.css_select(self.rule)[int(self.index)].text
                )

        elif self.method == 'text_content':
            self._set_element(
                lambda: self.css_select(self.rule)[int(self.index)].text_content()
                )

        # This makes it backwards compatible to V0.1.14 for original "attr" unless JQuery statements have been used
        elif self.method == 'get' or self.attr is not None:
            self._set_element(
                lambda: self.css_select(self.rule)[int(self.index)].get(self.attr)
                )

        elif self.method == 'dict' or self.attr is not None:
            self._set_element(
                lambda: dict(self.css_select(self.rule)[int(self.index)].attrib)
                )

        elif self.method == 'itertext':
            """
                Iterate through an ul li list to get a list of li elements
            """
            self._set_element(
                lambda: list(
                            filter(None, 
                                [Manipulation.clean_string(line) for line in self.css_select(self.rule)[int(self.index)].itertext()]
                        )
                    )
                )

        # We need the list element for the list_dict element to work
        elif self.method == 'list' or 'table':
            """
                Iterate through all elements found in page and return as a list
            """
            self._set_element(
                lambda: [el.text_content() for el in self.css_select(self.rule)]
                )

        if self.method == 'table':
            """
                Iterate through all elements found in a page that has a list with an even number like a table (td)
                and pair the values as key, value pairs and return as a dict
                
                table_dict = dict()
                for idx, item in enumerate(table):
                    # if Uneven it's a key, even is a value
                    if not idx % 2:
                        table_dict[item] = table[idx+1]
            """
            if isinstance(self.page_element, list) and (len(self.page_element) % 2) == 0:
                clean = Manipulation.clean_string
                self._set_element(
                    lambda: {
                        clean(self.page_element[idx-1]):clean(value) for idx, value in enumerate(self.page_element) if idx % 2
                        }
                    )
            else:
                logger.error(
                    "Object is a list: {} and the length must be even: {}. Both values must be true or else it is not a valid table. \
                    Validate your selector and the source code.".format(
                        isinstance(self.page_element, list),  (len(self.page_element) % 2) == 0
                    )
                )

        # manipulations
        if len(self.manipulate):
            for m in self.manipulate:
                if m in manipulation_options:
                    manipulate = getattr(Manipulation, m)
                    self.page_element = manipulate(self.page_element)
                else:
                    logger.error('Manipulation of type: "{}" is not known to the system. These are the options you can use: {}'.format(
                        m, ', '.join(manipulation_options)
                        )
                    )

        return self.page_element


class Xpath(Selector):
    def parse_detail(self, html):
        d = etree.HTML(html)
        try:
            if self.attr is None:
                if len(d.xpath(self.rule)) > 1:
                    return [entry.text for entry in d.xpath(self.rule)]
                else:
                    return d.xpath(self.rule)[0].text
            return [entry.get(self.attr, None) for entry in d.xpath(self.rule)] if len(d.xpath(self.rule)) > 1 else \
                d.xpath(self.rule)[0].text
        except IndexError:
            return None


class Regex(Selector):
    def parse_detail(self, html):
        try:
            return re.findall(self.rule, html)[0]
        except IndexError:
            return None
