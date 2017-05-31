class Spider:
    start_url = ''
    follow_urls = []
    parsers = []

    @classmethod
    def run(cls):
        for parser in cls.parsers:
            parser.parse()
