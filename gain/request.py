import asyncio

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
semaphore = asyncio.Semaphore(10)


async def fetch(url, session):
    print('Fetching {}'.format(url))

    with (await semaphore):
        async with session.get(url) as response:
            data = await response.text()
            return data
