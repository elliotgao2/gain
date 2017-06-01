from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.title a')
    # url = Css('.title a', 'href')
    points = Css('.subtext .score')

    def save(self):
        print(self.results)


# class User(Item):
#     username = Css('.username')
#     karma = Xpath('//[@class=karma]')
#
#     def save(self):
#         print(self.results)


class MySpider(Spider):
    start_url = 'https://news.ycombinator.com/'
    parsers = [Parser('/news?p=\d+'),
               Parser('/item?id=\d+', Post)]


MySpider.start()
