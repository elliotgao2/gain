import pytest
import asyncio
import pathlib
import socket
import ssl
import sys
# async yield not possible with python 3.5
from async_generator import async_generator, yield_
# from aiohttp.test_utils import unused_port
import aiohttp
from aiohttp import web
#  For fake Server
from datetime import datetime
import random
# For redis test
import hashlib

from gain.request import fetch
from utils.spider import FakeCacheSpider, cache
from utils.resolver import FakeResolver


html_raw = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Title of the document</title>
    </head>

    <body>
        {}
    </body>
    </html>
"""

alinea = """
        <p class="test">
            Content of the document: {}
        </p>
"""

count = """
        <p class="request_count">
            {}
        </p>
"""

random.seed(1)


class RedisCacheServer:

    def __init__(self, *, loop):
        self.loop = loop
        self.app = web.Application()
        
        self.app.router.add_routes(
            [web.get("/{name}", self.redis_cache_call),
             web.get("/calls", self.redis_cache_call)])

        self.handler = None
        self.server = None
        here = pathlib.Path(__file__)
        ssl_cert = here.parent / 'server.crt'
        ssl_key = here.parent / 'server.key'
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))

    async def start(self):
        # port = unused_port()
        port = 8080
        host = "localhost"
        self.handler = self.app._make_handler()
        self.server = await self.loop.create_server(self.handler,
                                                    '127.0.0.1', port,
                                                    ssl=self.ssl_context
                                                    )
        return {'{}'.format(host): port}

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        await self.app.shutdown()
        await self.handler.shutdown()
        await self.app.cleanup()

    async def redis_cache_call(self, request):
        headers = {"content_type": "text/html"}
        n = datetime.now().isoformat()
        delay = random.randint(0, 3)
        request_count = await cache.get('request_count')

        if not request_count:
            request_count = 0
            await cache.set('request_count', request_count)
        
        if request.raw_path == "/calls":
            html = html_raw.format(count.format(request_count))

            print("{}: {}\n\n test".format(n, request.path))
        else:
            headers = {"content_type": "text/html", "delay": str(delay)}
            request_count +=1
            await cache.set('request_count', request_count)
            name = request.match_info.get("name", "foo")
            html = html_raw.format(alinea.format(name))

            print("{}: {} delay: {}".format(n, request.path, delay))

        return web.Response(body=html, headers=headers)


@async_generator
@pytest.fixture()
async def info(loop):
    fake_redis_cache_server = RedisCacheServer(loop=loop)
    info = await fake_redis_cache_server.start()
    await yield_(info)
    await fake_redis_cache_server.stop()
    
@async_generator
@pytest.fixture()
async def session(loop, info):
    resolver = FakeResolver(info, loop=loop)
    connector = aiohttp.TCPConnector(loop=loop, resolver=resolver, ssl=False)
    session = aiohttp.ClientSession(connector=connector, loop=loop)
    await yield_(session)
    await session.close()


@pytest.mark.skipif(sys.version_info < (3,6),
                    reason="requires python3.6 and up")
async def test_redis_cache_hits(session):

    url = None
    tasks = []
    semaphore = asyncio.Semaphore(1)
    random_hash = hashlib.md5(str(datetime.now().isoformat()).encode("UTF-8")).hexdigest()
    spider = FakeCacheSpider()

    async with session:
        # Create cache
        for i in (random_hash,)*5:
            url = "https://localhost:8080/{}"
            html = await fetch(url.format(i), spider, session, semaphore)

        # Check count of non cached hits
        url = "https://localhost:8080/calls"
        _request_count = await fetch(url, spider, session, semaphore)

    request_count = [int(s) for s in _request_count.split() if s.isdigit()]

    assert request_count[0] == 1
