import asyncio
from datetime import datetime
from aiohttp import web
import random
from aiocache import SimpleMemoryCache

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
cache = SimpleMemoryCache()

async def handle(request):
    headers = {"content_type": "text/html"}
    n = datetime.now().isoformat()
    delay = random.randint(0, 3)

    request_count = await cache.get('request_count')

    if not request_count:
        request_count = 0
        await cache.set('request_count', request_count)
    
    if request.raw_path == "/calls":
        html = html_raw.format(count.format(request_count))

        print("{}: {}".format(n, request.path))
    else:
        headers = {"content_type": "text/html", "delay": str(delay)}
        request_count +=1
        await cache.set('request_count', request_count)
        name = request.match_info.get("name", "foo")

        await asyncio.sleep(delay) # Delay or else request are too fast
        html = html_raw.format(alinea.format(name))

        print("{}: {} delay: {}".format(n, request.path, delay))

    return web.Response(body=html, headers=headers)


def start_server():
    app = web.Application()
    app.router.add_route("GET", "/{name}", handle)
    app.router.add_route("GET", "/calls", handle)
    web.run_app(app)


if __name__ == "__main__":
    start_server()