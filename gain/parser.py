import re
from pybloomfilter import BloomFilter

import requests


class Parser:
    def __init__(self, rule, item=None):
        self.rule = rule
        self.item = item
        self.parsing_urls = []
        self.parsed_urls = BloomFilter(10000000, 0.01)

    def add(self, urls):
        url = '{}'.format(urls)
        if url.encode('utf-8') not in self.parsed_urls:
            self.parsed_urls.add(url.encode('utf-8'))
            self.parsing_urls.append(url)

    def parse_urls(self, html):
        urls = re.findall(self.rule, html)
        for url in urls:
            self.add(url)

    def parse_item(self, html):
        item = self.item(html)
        item.save()
        return item

    def task(self, spider):
        while len(self.parsing_urls) > 0:
            url = self.parsing_urls.pop()
            print(url)
            html = requests.get(url).text
            spider.parse(html)
