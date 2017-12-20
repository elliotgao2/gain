from gain import Item, Parser, Spider, Xpath


class Post(Item):
    quote = Xpath("//span[@class = 'text']")
    author = Xpath("//small")

    async def save(self):
        quote = dict(zip(self.author, self.quote))
        assert quote['Albert Einstein'] == '“Try not to become a man of success. Rather become a man of value.”'


class MySpider(Spider):
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    start_url = 'http://quotes.toscrape.com/'
    parsers = [Parser('/page/1/'),
               Parser('/page/1/', Post)]

MySpider.run()

