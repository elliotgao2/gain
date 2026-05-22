from .log import logger


async def fetch(url, spider, session, semaphore):
    async with semaphore:
        try:
            headers = spider.headers() if callable(spider.headers) else spider.headers
            async with session.get(url, headers=headers, proxy=spider.proxy) as response:
                if response.status in (200, 201):
                    return await response.text()
                logger.error(f"Error: {url} {response.status}")
                return None
        except Exception:
            return None
