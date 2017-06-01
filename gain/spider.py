import asyncio

import requests
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Spider:
    start_url = ''
    parsers = []

    @classmethod
    def parse(cls, html):
        for parser in cls.parsers:
            if parser.item is not None:
                parser.parse_item(html)
            parser.parse_urls(html)

    @classmethod
    def run(cls):
        html = requests.get(cls.start_url).text
        cls.parse(html)
        for parser in cls.parsers:
            parser.task(cls)

    @classmethod
    def start(cls):
        print('starting...')
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(cls.run())
        loop.run_until_complete(future)
