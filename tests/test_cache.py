import asyncio
import aiohttp
import hashlib
from gain.request import fetch
from gain import Spider
from aiocache import caches
from datetime import datetime


class FakeCacheSpider:
    proxy = None
    cache_enabled = True
    cache_alias = Spider.cache_alias
    cache_config = Spider.cache_config
    caches = None
    headers = None
    cache_disabled_urls = ["http://localhost:8080/calls"]

    def __init__(self):
        if caches and not self.caches:
            if self.cache_enabled and self.cache_config:
                caches.set_config(self.cache_config)
                self.caches = caches

async def validate():
    # We do not want the validate request to be done after all tasks are finished
    await asyncio.sleep(1) # Delay or else request are too fast

    url = "http://localhost:8080/calls"
    semaphore = asyncio.Semaphore(1)

    async with aiohttp.ClientSession() as session:
        return await fetch(url, FakeCacheSpider(), session, semaphore)

async def run():

    url = "http://localhost:8080/{}"
    tasks = []
    semaphore = asyncio.Semaphore(1)
    random_hash = hashlib.md5(str(datetime.now().isoformat()).encode("UTF-8")).hexdigest()

    async with aiohttp.ClientSession() as session:

        for i in (random_hash,)*5:
            html = await fetch(url.format(i), FakeCacheSpider(), session, semaphore)
    
    _request_count = await validate()

    request_count = [int(s) for s in _request_count.split() if s.isdigit()]

    assert request_count[0] == 1


# def test_validate_cache():
#     """
#         Docker Redis and Webserver.py needs to be running.
#     """
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(run())
#     loop.run_until_complete(future)
#     loop.close()

# if __name__ == "__main__":
#     test_validate_cache()