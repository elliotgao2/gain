import asyncio
import re
from html import unescape

import aiohttp

from gain.request import fetch
from .log import logger


class Parser:
    def __init__(self, rule, item=None):
        self.rule = rule
        self.item = item
        self.parsing_urls = []
        self.pre_parse_urls = []
        self.filter_urls = set()
        self.done_urls = []

    def add(self, urls):
        url = '{}'.format(urls)
        if url not in self.filter_urls:
            self.filter_urls.add(url)
            self.pre_parse_urls.append(url)

    def parse_urls(self, html, base_url):
        if html is None:
            return
        urls = re.findall(self.rule, html)
        for url in urls:
            url = unescape(url)
            if not re.match('(http|https)://', url):
                url = base_url + url
            self.add(url)

    def parse_item(self, html):
        item = self.item(html)
        return item

    async def execute_url(self, url, spider, session, semaphore):
        html = await fetch(url, spider, session, semaphore)

        if html is None:
            spider.error_urls.append(url)
            self.pre_parse_urls.append(url)
            return None

        if url in spider.error_urls:
            spider.error_urls.remove(url)
        spider.urls_count += 1
        self.parsing_urls.remove(url)
        self.done_urls.append(url)

        if self.item is not None:
            item = self.parse_item(html)
            await item.save()
            self.item.count_add()
            logger.info('Parsed({}/{}): {}'.format(len(self.done_urls), len(self.filter_urls), url))
        else:
            spider.parse(html)
            logger.info('Followed({}/{}): {}'.format(len(self.done_urls), len(self.filter_urls), url))

    async def task(self, spider, semaphore):
        with aiohttp.ClientSession() as session:
            while spider.is_running():
                if len(self.pre_parse_urls) == 0:
                    await asyncio.sleep(0.5)
                    continue
                url = self.pre_parse_urls.pop()
                self.parsing_urls.append(url)
                asyncio.ensure_future(self.execute_url(url, spider, session, semaphore))
