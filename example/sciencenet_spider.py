from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.ph')

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = 'http://blog.sciencenet.cn/home.php?mod=space&uid=40109&do=blog&view=me&from=space'
    concurrency = 1
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('http://blog.sciencenet.cn/home.php\?mod=space&uid=\d+&do=blog&view=me&from=space&page=\d+'),
               Parser('blog\-\d+\-\d+\.html', Post)]


MySpider.run()
