# import asyncio
# import aiohttp
# from gain.request import fetch


# async def run(r):
#     class FakeSpider():
#         proxy = None
#         cache_enabled = True
#         cache_alias = "default"
#         cache_config = {
#             'default': {
#                 'cache': "aiocache.SimpleMemoryCache",
#                 'serializer': {
#                     'class': "aiocache.serializers.StringSerializer"
#                 }
#             }
#         }

#     url = "http://localhost:8080/{}"
#     tasks = []
#     semaphore = asyncio.Semaphore(2)

#     async with aiohttp.ClientSession() as session:

#         for i in [1,2,1,2,1,2,1,2,3,4]:
#             task = asyncio.ensure_future(fetch(url, FakeSpider, session, semaphore))
#             tasks.append(task)

#         responses = asyncio.gather(*tasks)
#         data = await responses

# number = 10
# loop = asyncio.get_event_loop()

# future = asyncio.ensure_future(run(number))
# loop.run_until_complete(future)


from gain import Item, Parser, Spider, Xpath

class Post(Item):
    quote = Xpath("//span[@class = 'text']")
    author = Xpath("//small")

    async def save(self):
        quote = dict(zip(self.author, self.quote))
        assert quote['Albert Einstein'] == "“If you can't explain it to a six year old, you don't understand it yourself.”"

class MySpider(Spider):
    concurrency = 5
    cache_enabled = True
    headers = {'User-Agent': 'Google Spider'}
    start_url = 'http://quotes.toscrape.com/'
    parsers = [Parser('/page/2/'),
               Parser('/page/2/', Post),
               Parser("/page/2/")]

    use_cache = True

MySpider.run()
