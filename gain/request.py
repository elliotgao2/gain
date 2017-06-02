import asyncio

import aiohttp
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def fetch(url, semaphore):
    with (await semaphore):
        print(semaphore)
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                return data
