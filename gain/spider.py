class Spider:
    start_url = ''
    parsers = []
    follow_selectors = []

    follow_urls = []
    followed_urls = []

    @classmethod
    def run(cls):
        for follow_url in cls.follow_urls:
            html = ''
            for parser in cls.parsers:
                parser.parse_urls.append(parser.selector.parse(html))
            for follow_selector in cls.follow_selectors:
                cls.follow_urls.append(follow_selector.parse(html))
                cls.followed_urls.append(follow_url)
