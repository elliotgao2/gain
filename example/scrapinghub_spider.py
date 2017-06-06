from gain import Css, Item, Parser, Regex, Spider


class Post(Item):
    title = Css('.entry-title')
    content = Css('.entry-content')
    regex_test = Regex('\d+')

    async def save(self):
        print(self.title, '\n')


class MySpider(Spider):
    start_url = 'https://blog.scrapinghub.com/'
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
               Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/', Post)]


MySpider.run()
