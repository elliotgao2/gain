import re


class Spider:
    start_url = ''
    parsers = []
    follow_rules = []

    following_urls = []
    followed_urls = []

    @classmethod
    def parse_urls(cls, html):
        for rule in cls.follow_rules:
            urls = re.findall(rule, html)
            for url in urls:
                if url not in cls.followed_urls:
                    cls.following_urls.append(urls)
                    cls.followed_urls.append(urls)

    @classmethod
    def run(cls):
        while len(cls.following_urls) != 0:
            url = cls.following_urls.pop()
            html = url
            cls.parse_urls(html)
            for parser in cls.parsers:
                parser.parse_urls(html)
            cls.following_urls.remove(url)
