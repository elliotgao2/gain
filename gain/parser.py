import asyncio
import re
from pybloomfilter import BloomFilter

from gain.request import fetch


class Parser:
    def __init__(self, rule, item=None):
        self.rule = rule
        self.item = item
        self.parsing_urls = []
        self.filter_urls = BloomFilter(10000000, 0.01)
        self.done_urls = []

    def add(self, urls):
        url = '{}'.format(urls)
        if url.encode('utf-8') not in self.filter_urls:
            self.filter_urls.add(url.encode('utf-8'))
            self.parsing_urls.append(url)

    def parse_urls(self, html):
        urls = re.findall(self.rule, html)
        for url in urls:
            self.add(url)

    def parse_item(self, html):
        item = self.item(html)
        item.save()
        return item

    async def execute_url(self, spider, semaphore, url):

        html = await fetch(url, semaphore)
        print('({}/{}) {}'.format(len(self.done_urls), len(self.parsing_urls), url))

        if self.item is not None:
            self.parse_item(html)
        spider.parse(html)
        self.done_urls.append(url)

    async def task(self, spider, semaphore):
        while True:
            if len(self.parsing_urls) <= 0:
                break
            url = self.parsing_urls.pop()
            asyncio.ensure_future(self.execute_url(spider, semaphore, url))
