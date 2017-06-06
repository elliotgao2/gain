from gain import Css, Item, Parser, Xpath


def test_parse():
    html = '<title class="username">tom</title><div class="karma">15</div>'

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser('http://github.com', User)

    user = parser.parse(html)
    assert 'username' in user.results
    assert 'karma' in user.results
    assert user.username == 'tom'
    assert user.karma == '15'


def test_parse_urls():
    html = ('<a href="item?id=14447885">64comments</a>'
            '<a href="item?id=14447886">64comments</a>')

    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    parser = Parser('item\?id=\d+', User)
    parser.parse_urls(html)
    assert parser.parsing_urls.__len__() == 2
    assert 'item?id=14447886' in parser.parsing_urls
    assert 'item?id=14447885' in parser.parsing_urls

    assert 'item?id=14447886' in parser.parsed_urls
    assert 'item?id=14447885' in parser.parsed_urls
