class Parser:
    def __init__(self, url, item):
        self.item = item
        self.url = url

    def parse(self):
        self.item(self.url).save()
