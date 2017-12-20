## Step 1. define item

```python
from gain import Css, Item
from gain.result import FileResult

class Post(Item):
    __result__ = FileResult("file:///scrapinghub.txt")
    title = Css('.entry-title')
    content = Css('.entry-content')
```

The name is "Post" 
The keys are "title" and "content".
The value is the css selector or xpath selector.
`result_cls`: save data.

## Spider

```python
from gain import Parser, Spider

class MySpider(Spider):
    start_url = 'https://blog.scrapinghub.com/'
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
               Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/', Post)]


MySpider.run()
```

Inherit the gain.Spider class. And do some config.
The "start_url" means the starting point.
The "concurrency" means the concurrent quantity.
The "parsers" is a list of `gain.Paser` instance.
A gain.Parser instance describe how the spider works.
A Parser instance with one parameter means following the urls.
A Parser instance with two parameters means parsing items.

