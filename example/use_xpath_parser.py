from gain import Css, Item, Parser, XPathParser, Spider


class Post(Item):
    title = Css('.breadcrumb_last')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'https://mydramatime.com/europe-and-us-drama/'
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    parsers = [
               XPathParser('//span[@class="category-name"]/a/@href'),
               XPathParser('//div[contains(@class, "pagination")]/ul/li/a[contains(@href, "page")]/@href'),
               XPathParser('//div[@class="mini-left"]//div[contains(@class, "mini-title")]/a/@href', Post)
              ]


if __name__ == '__main__':
    MySpider.run()
