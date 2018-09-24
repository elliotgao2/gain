import asyncio
import re
from datetime import datetime

import aiohttp
from gain.request import fetch

import logging as logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

try:
    from aiocache import caches
except ImportError:
    logger.info("Install aiocache to use cache: pipenv install aiocache")


class Spider:
    start_url = ''
    base_url = None
    parsers = []
    error_urls = []
    urls_count = 0
    concurrency = 5
    interval = None #Todo: Limit the interval between two requests
    headers = {}
    proxy = None
    cookie_jar = None
    caches = None
    cache_enabled = False
    cache_disabled_urls = []
    cache_alias = "default"
    cache_config = {
        'default': {
            'cache': "aiocache.RedisCache",
            'endpoint': "127.0.0.1",
            'port': 6379,
            'timeout': 1,
            'serializer': {
                'class': "aiocache.serializers.PickleSerializer"
            }
        }
    }

    test = False
    test_class = None
    limit_requests = False
    max_requests = 1

    @classmethod
    def init_caches(cls):
        if caches and not cls.caches:
            if cls.cache_enabled and cls.cache_config:
                caches.set_config(cls.cache_config)
                cls.caches = caches

    @classmethod
    def is_running(cls):
        is_running = False
        cancel = False

        if cls.test:
            parser_stats = {parser.item.name:parser.item.count for parser in cls.parsers if parser.item is not None}
            for k, v in parser_stats.items():
                if v >= cls.max_requests:
                    cancel = True
                else:
                    cancel = False
            try:
                if cls.test_class and parser_stats[cls.test_class] >= cls.max_requests:
                    cancel = True
            except KeyError:
                logger.error('Your test class "{}" does not exist.'.format(cls.test_class))

        # Limits actuall requests
        if cls.limit_requests and cls.urls_count >= cls.max_requests:
            cancel = True

        if cancel:
            cls.cancel_all()

        for parser in cls.parsers:
            if not parser.pre_parse_urls.empty() or len(parser.parsing_urls) > 0:
                is_running = True

        return is_running

    @classmethod
    def parse(cls, html):
        for parser in cls.parsers:
            parser.parse_urls(html, cls.base_url)

    @classmethod
    def run(cls):
        cls.init_caches()
        logger.info('Spider started!')
        start_time = datetime.now()
        loop = asyncio.get_event_loop()

        if cls.base_url is None:
            cls.base_url = re.match('(http|https)://[\w\-_]+(\.[\w\-_]+)+/', cls.start_url).group()
            logger.info('Base url: {}'.format(cls.base_url))
        try:
            semaphore = asyncio.Semaphore(cls.concurrency)
            tasks = asyncio.wait([parser.task(cls, semaphore) for parser in cls.parsers])
            loop.run_until_complete(cls.init_parse(semaphore))
            loop.run_until_complete(tasks)
            # Close loop in try, it's async so comes after final
            loop.close() 
        except (KeyboardInterrupt, SystemExit, asyncio.CancelledError):
            cls.cancel_all()
        finally:
            end_time = datetime.now()
            for parser in cls.parsers:
                if parser.item is not None:
                    logger.info('Item "{}": {}'.format(parser.item.name, parser.item.count))
            logger.info('Requests count: {}'.format(cls.urls_count))
            logger.info('Error count: {}'.format(len(cls.error_urls)))
            logger.info('Time usage: {}'.format(end_time - start_time))
            logger.info('Spider finished!')

    @staticmethod 
    def cancel_all():
        for task in asyncio.Task.all_tasks():
            task.cancel()

    @classmethod
    async def init_parse(cls, semaphore):
        cls.init_caches()
        async with aiohttp.ClientSession(cookie_jar=cls.cookie_jar) as session:
            html = await fetch(cls.start_url, cls, session, semaphore)
            cls.parse(html)
