import asyncio

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


async def fetch(url, session, semaphore):
    with (await semaphore):
        try:
            async with session.get(url) as response:
                if response.status in [200, 201]:
                    data = await response.text()
                    return data
                return None
        except:
            return None
