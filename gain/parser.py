import asyncio
from asyncio import Queue
import re
from html import unescape
from urllib.parse import urljoin

import aiohttp
from lxml import etree

from gain.request import fetch
from .log import logger


class BaseParser(object):    
    def __init__(self, rule, item=None):
        self.rule = rule
        self.item = item
        self.parsing_urls = []
        self.pre_parse_urls = Queue()
        self.filter_urls = set()
        self.done_urls = []

    def parse_urls(self, html, base_url):
        if html is None:
            return
        for url in self.abstract_urls(html):
            url = unescape(url)
            if not re.match('(http|https)://', url):
                url = urljoin(base_url, url)
            self.add(url)
    
    def abstract_urls(self, html):
        raise NotImplementedError

    def add(self, urls):
        url = '{}'.format(urls)
        if url not in self.filter_urls:
            self.filter_urls.add(url)
            self.pre_parse_urls.put_nowait(url)

    def parse_item(self, html):
        item = self.item(html)
        return item

    async def execute_url(self, url, spider, session, semaphore):
        html = await fetch(url, spider, session, semaphore)

        if html is None:
            spider.error_urls.append(url)
            self.pre_parse_urls.put_nowait(url)
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
        async with aiohttp.ClientSession(cookie_jar=spider.cookie_jar) as session:
            while spider.is_running():
                try:
                    url = await asyncio.wait_for(self.pre_parse_urls.get(), 5)
                    self.parsing_urls.append(url)
                    asyncio.ensure_future(self.execute_url(url, spider, session, semaphore))
                except asyncio.TimeoutError:
                    pass


class Parser(BaseParser):
    def abstract_urls(self, html):
        urls = re.findall(self.rule, html)
        return urls


class XPathParser(BaseParser):
    def abstract_urls(self, html):
        doc = etree.HTML(html)
        urls = doc.xpath(self.rule)
        return urls
