import asyncio
import re
from pybloomfilter import BloomFilter

from gain.request import fetch


class Parser:
    def __init__(self, rule, item=None):
        self.rule = rule
        self.item = item
        self.parsing_urls = asyncio.Queue()
        self.parsed_urls = BloomFilter(10000000, 0.01)

    def add(self, urls):
        print(urls)
        url = '{}{}'.format('https://news.ycombinator.com/', urls)
        if bytes(url) not in self.parsed_urls:
            self.parsed_urls.append(bytes(url))
            self.parsing_urls.put_nowait(url)

    def parse_urls(self, html):
        urls = re.findall(self.rule, html)
        for url in urls:
            self.add(url)

    def parse_item(self, html):
        item = self.item(html)
        item.save()
        return item

    async def task(self, spider, session):
        while not self.parsing_urls.empty():
            if len(self.parsed_urls) > 10:
                break
            url = await self.parsing_urls.get()
            html = await fetch(url, session)
            await spider.parse(html)
