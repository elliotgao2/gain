import asyncio

import uvloop
from aiohttp import ClientSession

from gain.request import fetch

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Spider:
    start_url = ''
    parsers = []

    @classmethod
    def parse(cls, html):
        for parser in cls.parsers:
            if parser.item is None:
                parser.parse_urls(html)
            else:
                parser.parse_item(html)

    @classmethod
    async def run(cls):
        tasks = []
        async with ClientSession() as session:
            html = await fetch(cls.start_url, session)
            cls.parse(html)
            for parser in cls.parsers:
                tasks.append(asyncio.ensure_future(parser.task(cls, session)))
            await asyncio.gather(*tasks)

    @classmethod
    def start(cls):
        print('starting...')
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(cls.run())
        loop.run_until_complete(future)
