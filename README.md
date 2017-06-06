# Gain

[![Python](https://img.shields.io/pypi/pyversions/gain.svg)](https://pypi.python.org/pypi/gain/)
[![Version](https://img.shields.io/pypi/v/gain.svg)](https://pypi.python.org/pypi/gain/)
[![License](https://img.shields.io/pypi/l/gain.svg)](https://pypi.python.org/pypi/gain/)

Web crawling framework for everyone. Written with asyncio, uvloop and aiohttp.
Everyone could write their own web crawler easily with gain framework. Gain framework provide a pretty simple api.

## Requirements

- Python3.5+

## Installation

`pip install gain`

`pip install uvloop` (Only linux)

## Usage

1. Write spider.py:

```python
from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css('.entry-title')
    content = Css('.entry-content')

    async def save(self):
        with open('scrapinghub.txt', 'a+') as f:
            f.writelines(self.results['title'] + '\n')


class MySpider(Spider):
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    start_url = 'https://blog.scrapinghub.com/'
    parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
               Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/', Post)]


MySpider.run()
```
2. Run `python spider.py`

3. Result:

![](img/sample.png)

## Example

The examples are in the `/example/` directory.

## Contribution

- Pull request.
- Open issue.