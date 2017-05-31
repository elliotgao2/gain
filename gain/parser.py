class Parser:
    def __init__(self, selector, item):
        self.selector = selector
        self.item = item
        self.parse_urls = []
        self.history_urls = []

    def parse(self, html):
        self.item(html).save()

    def listen(self):
        for parse_url in self.parse_urls:
            self.history_urls.append(parse_url)
            self.parse(parse_url)
