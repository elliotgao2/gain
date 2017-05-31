import re


class Parser:
    def __init__(self, rule, item):
        self.rule = rule
        self.item = item
        self.parsing_urls = []
        self.parsed_urls = []

    def parse(self, html):
        item = self.item(html)
        item.save()
        return item

    def parse_urls(self, html):
        urls = re.findall(self.rule, html)
        for url in urls:
            if url not in self.parsed_urls:
                self.parsing_urls.append(url)
                self.parsed_urls.append(url)

    def listen(self):
        while len(self.parsing_urls) != 0:
            url = self.parsed_urls.pop()
            self.parse(url)
            self.parsing_urls.remove(url)
