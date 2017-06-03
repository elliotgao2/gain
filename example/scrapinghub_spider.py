from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.entry-title')
    content = Css('.entry-content')

    async def save(self):
        with open('scrapinghub.txt', 'a+') as f:
            f.writelines(self.results['title'] + '\n')


class MySpider(Spider):
    start_url = 'https://blog.scrapinghub.com/'
    frequency = 5
    parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
               Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/', Post)]


MySpider.run()
