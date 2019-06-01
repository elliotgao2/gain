from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css('h1')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'https://///www.v2ex.com/go//////create'  # change here, if you want to scrape this site.
    concurrency = 1
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('/go/create?p=\d+'),
               Parser('/t/\d+#reply\d+', Post)]


MySpider.run()
