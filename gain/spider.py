import asyncio
import re
from datetime import datetime

import aiohttp

from gain.request import fetch

from .log import logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider:
    start_url = ""
    base_url = None
    parsers = []
    error_urls = []
    urls_count = 0
    concurrency = 5
    interval = None
    headers = {}
    proxy = None
    cookie_jar = None

    @classmethod
    def is_running(cls):
        return any(
            not parser.pre_parse_urls.empty() or len(parser.parsing_urls) > 0
            for parser in cls.parsers
        )

    @classmethod
    def parse(cls, html):
        for parser in cls.parsers:
            parser.parse_urls(html, cls.base_url)

    @classmethod
    def run(cls):
        logger.info("Spider started!")
        start_time = datetime.now()
        try:
            asyncio.run(cls._run())
        finally:
            end_time = datetime.now()
            for parser in cls.parsers:
                if parser.item is not None:
                    logger.info(f'Item "{parser.item.name}": {parser.item.count}')
            logger.info(f"Requests count: {cls.urls_count}")
            logger.info(f"Error count: {len(cls.error_urls)}")
            logger.info(f"Time usage: {end_time - start_time}")
            logger.info("Spider finished!")

    @classmethod
    async def _run(cls):
        if cls.base_url is None:
            cls.base_url = re.match(r"(http|https)://[\w\-_]+(\.[\w\-_]+)+/", cls.start_url).group()
            logger.info(f"Base url: {cls.base_url}")
        semaphore = asyncio.Semaphore(cls.concurrency)
        await cls.init_parse(semaphore)
        tasks = [asyncio.create_task(parser.task(cls, semaphore)) for parser in cls.parsers]
        try:
            await asyncio.gather(*tasks)
        except (KeyboardInterrupt, asyncio.CancelledError):
            for task in tasks:
                task.cancel()
            raise

    @classmethod
    async def init_parse(cls, semaphore):
        async with aiohttp.ClientSession(cookie_jar=cls.cookie_jar) as session:
            html = await fetch(cls.start_url, cls, session, semaphore)
            cls.parse(html)
