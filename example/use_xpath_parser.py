from gain import Css, Item, Parser, XPathParser, Spider


class Post(Item):
    title = Css('.breadcrumb_last')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'https://mydramatime.com/europe-and-us-drama/game-of-thrones/'
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('https://mydramatime.com/europe-and-us-drama/game-of-thrones/page/\d+?/'),
               XPathParser('//div[@class="mini-left"]//div[contains(@class, "mini-title")]/a/@href', Post)]


if __name__ == '__main__':
    MySpider.run()
