import re

from lxml import etree
from pyquery import PyQuery as pq


class Selector:
    def __init__(self, rule, attr=None):
        self.rule = rule
        self.attr = attr

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def parse_detail(self, html):
        raise NotImplementedError


class Css(Selector):
    def parse_detail(self, html):
        d = pq(html)
        if self.attr is None:
            try:
                return d(self.rule)[0].text
            except IndexError:
                return None
        return d(self.rule)[0].attr(self.attr, None)


class Xpath(Selector):
    def parse_detail(self, html):
        d = etree.HTML(html)
        try:
            if self.attr is None:
                return d.xpath(self.rule)[0].text
            return d.xpath(self.rule)[0].get(self.attr, None)
        except IndexError:
            return None


class Regex(Selector):
    def parse_detail(self, html):
        try:
            return re.findall(self.rule, html)[0]
        except IndexError:
            return None
