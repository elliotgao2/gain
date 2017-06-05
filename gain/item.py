from .log import logger
from .selector import Selector


class ItemType(type):
    def __new__(mcs, name, bases, namespace):
        selectors = {}
        namespace['_item_name'] = name
        namespace['_item_count'] = 0
        for name, value in namespace.items():
            if isinstance(value, Selector):
                selectors[name] = value
        namespace['selectors'] = selectors
        for name, value in selectors.items():
            del namespace[name]
        return type.__new__(mcs, name, bases, namespace)


class Item(metaclass=ItemType):
    def __init__(self, html):
        self.results = {}
        for name, selector in self.selectors.items():
            value = selector.parse_detail(html)
            if value is None:
                logger.error('Selector "{}" for {} was wrong, please check again'.format(selector.rule, name))
            else:
                self.results[name] = value

    def __getattr__(self, item):
        if item not in self.results:
            raise AttributeError
        return self.results[item]

    async def save(self):
        raise NotImplementedError
