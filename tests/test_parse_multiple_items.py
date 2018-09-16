from gain import Item, Parser, Spider, Xpath

class Post(Item):
    quote = Xpath("//span[@class = 'text']")
    author = Xpath("//small")

    async def save(self):
        quote = dict(zip(self.author, self.quote))
        assert quote['Albert Einstein'] == "“If you can't explain it to a six year old, you don't understand it yourself.”"

class MySpider(Spider):
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    start_url = 'http://quotes.toscrape.com/'
    parsers = [Parser('/page/2/', Post)]

MySpider.run()
