from gain import Css, Item, Parser, Regex, Spider, Xpath


class Post(Item):
    id = Regex('')
    title = Css('')
    username = Css('')
    url = Css('')
    points = Xpath('')

    def save(self):
        print(self.results)


class User(Item):
    id = Regex('\d+')
    username = Css('.username')
    karma = Xpath('//[@class=karma]')

    def save(self):
        print(self.results)


class MySpider(Spider):
    start_url = ''
    follow_urls = ['',
                   '']
    parsers = [Parser('', Post),
               Parser('', User)]


MySpider.run()
