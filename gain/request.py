import asyncio
import types

import logging as logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


def md5hash(string):
    import hashlib
    return hashlib.md5(string.encode("UTF-8")).hexdigest()

async def fetch(url, spider, session, semaphore):
    async def _request(url, spider, session, semaphore, proxy, cache):
        with (await semaphore):
            try:
                if callable(spider.headers):
                    headers = spider.headers()
                else:
                    headers = spider.headers
                async with session.get(url, headers=headers, proxy=proxy) as response:
                    if response.status in [200, 201]:
                        data = await response.text()

                        if spider.cache_enabled:
                            await cache.set(md5hash(url), data)

                        if cache: await cache.close()  # Close connection.
                        return data

                    logger.error('Error: {} {}'.format(url, response.status))
                    if cache: await cache.close()
                    return None
            except:
                if cache: await cache.close() 
                return None
    
    cache = None

    # Cache
    if spider.cache_enabled:
        cache = spider.caches.create(spider.cache_alias)

    # Proxy
    proxy = spider.proxy

    if proxy:
        if isinstance(spider.proxy, types.GeneratorType):
            proxy = next(spider.proxy)

    if spider.cache_enabled and url not in spider.cache_disabled_urls:
        url_hash = md5hash(url)

        # Validate Cache
        if await cache.exists(url_hash):

            logger.info('CACHE HIT: {}'.format(url))
            html = await cache.get(url_hash)
            
            # Not sure if we should keep this code for production
            # Or we should improve the task manager, to update the task to try again later.
            # It happens because of lack of intervalling in this project that sometimes we get no result and cache it
            if len(html) == 0:
                logger.info('CACHE HIT: the data seems corrupted so we cannot use the cache for {}'.format(url))
                return await _request(url, spider, session, semaphore, proxy, cache)
            else:
                await cache.close()
                return html
        else:
            return await _request(url, spider, session, semaphore, proxy, cache)
    else:
        return await _request(url, spider, session, semaphore, proxy, cache)