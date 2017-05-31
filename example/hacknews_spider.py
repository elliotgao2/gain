from gain import Css, Item, Parser, Spider, Xpath


class Post(Item):
    id = Css('')
    title = Css('')
    username = Css('')
    url = Css('')
    points = Xpath('')

    def save(self):
        print(self.results)


class User(Item):
    username = Css('.username')
    karma = Xpath('//[@class=karma]')

    def save(self):
        print(self.results)


class MySpider(Spider):
    start_url = ''
    follow_rules = ['',
                    '']
    parsers = [Parser('', Post),
               Parser('', User)]


MySpider.run()
