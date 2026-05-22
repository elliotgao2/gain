import aiofiles

from gain import Css, Item, Parser, Regex, Spider


class Post(Item):
    title = Css(".entry-title")
    content = Css(".entry-content")
    regex_test = Regex(r"\d+")

    async def save(self):
        async with aiofiles.open("scrapinghub.txt", "a+") as f:
            await f.write(str(self.results))


class MySpider(Spider):
    start_url = "https://blog.scrapinghub.com/"
    concurrency = 5
    headers = {"User-Agent": "Google Spider"}
    parsers = [
        Parser(r"https://blog.scrapinghub.com/page/\d+/"),
        Parser(r"https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/", Post),
    ]


MySpider.run()
