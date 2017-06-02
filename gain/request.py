import asyncio

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def fetch(url, session, semaphore):
    with (await semaphore):
            async with session.get(url) as response:
                data = await response.text()
                return data
