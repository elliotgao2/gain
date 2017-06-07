from gain import Css, Item, Parser, Xpath


def test_parse():
    html = '<title class="username">tom</title><div class="karma">15</div>'

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser(html, User)

    user = parser.parse_item(html)
    assert user.results == {
        'username': 'tom',
        'karma': '15'
    }


def test_parse_urls():
    html = ('<a href="item?id=14447885">64comments</a>'
            '<a href="item?id=14447886">64comments</a>')

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser('item\?id=\d+', User)
    parser.parse_urls(html, 'https://blog.scrapinghub.com')
    assert parser.pre_parse_urls.__len__() == 2
