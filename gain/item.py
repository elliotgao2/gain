from .selector import Selector


class ItemType(type):
    def __new__(mcs, name, bases, namespace):
        selectors = {}
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
            self.results[name] = selector.parse_detail(html)

    def __getattr__(self, item):
        if item not in self.results:
            raise AttributeError
        return self.results[item]

    def save(self):
        raise NotImplementedError
