from gain import Css, Item, Xpath


def test_item_define():
    class User(Item):
        username = Css('.username')
        karma = Xpath('//[@class=karma]')

    assert 'username' in User.selectors
    assert isinstance(User.selectors['username'], Css)
    assert 'karma' in User.selectors
    assert isinstance(User.selectors['karma'], Xpath)


def test_item_parse():
    class User(Item):
        username = Xpath('//title')
        karma = Css('.karma')

    html = '<title class="username">tom</title><div class="karma">15</div>'
    user = User(html)

    assert user.results == {
        'username': 'tom',
        'karma': '15'
    }
