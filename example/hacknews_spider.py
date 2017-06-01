from gain import Css, Item, Parser, Spider


class Post(Item):
    a = Css('title')

    def save(self):
        print(self.results)


class MySpider(Spider):
    start_url = 'https://movie.douban.com/'
    parsers = [Parser('/news?p=\d+'),
               Parser('https://movie.douban.com/subject/\d+/', Post)]


MySpider.run()
