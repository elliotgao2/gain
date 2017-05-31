import asyncio
import re

import aiohttp


class Spider:
    start_url = ''
    parsers = []
    follow_rules = []

    following_urls = []
    followed_urls = []

    @classmethod
    def parse_urls(cls, html):
        for rule in cls.follow_rules:
            urls = re.findall(rule, html)
            for url in urls:
                if url not in cls.followed_urls:
                    cls.following_urls.append(urls)
                    cls.followed_urls.append(urls)

    @classmethod
    def run(cls):
        while len(cls.following_urls) != 0:
            url = cls.following_urls.pop()
            html = url
            cls.parse_urls(html)
            for parser in cls.parsers:
                parser.parse_urls(html)
            cls.following_urls.remove(url)

        async def fetch(host):
            async with aiohttp.ClientSession(loop=loop) as session:
                async with session.get(host) as response:
                    print('{}'.format(response.status))
                    return await response.text()

        url = 'http://httpbin.org/ip'
        loop = asyncio.get_event_loop()
        tasks = [fetch(url) for i in range(20)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
