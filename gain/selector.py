class Selector:
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.rule)

    def parse(self, html):
        return 'Good'


class Css(Selector):
    """"""


class Xpath(Selector):
    """"""


class Regex(Selector):
    """"""
