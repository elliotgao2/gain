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
            parser.parse_urls(html)

    @classmethod
    def run(cls):
        cls.init_parse()
        print('starting...')

        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(5)

        tasks = asyncio.wait([parser.task(cls, semaphore) for parser in cls.parsers])
        loop.run_until_complete(tasks)

    @classmethod
    def init_parse(cls):
        html = requests.get(cls.start_url).text
        cls.parse(html)
