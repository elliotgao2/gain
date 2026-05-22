# Tutorial

Build a small crawler that grabs every post title from a paginated blog.

## 1. Install

```bash
pip install gain
```

Requires Python 3.10+.

## 2. Define an item

An `Item` describes one record. Field selectors pull values out of each
matched page.

```python
from gain import Css, Item


class Post(Item):
    title = Css(".entry-title")
    content = Css(".entry-content")

    async def save(self):
        print(self.title)
```

`save()` is your async hook — write to a file, push to a queue, insert into
a database, whatever you like.

## 3. Define a spider

A `Spider` ties one or more parsers to a `start_url`.

```python
from gain import Parser, Spider


class MySpider(Spider):
    concurrency = 5
    headers = {"User-Agent": "Google Spider"}
    start_url = "https://blog.scrapinghub.com/"
    parsers = [
        Parser(r"https://blog.scrapinghub.com/page/\d+/"),
        Parser(r"https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/", Post),
    ]
```

- A `Parser` with **one argument** *follows* every URL it matches — it
  doesn't extract anything, just queues the page for further parsing.
- A `Parser` with **two arguments** *extracts* an `Item` from every URL it
  matches.

## 4. Run

```python
MySpider.run()
```

That's it. `gain` opens an `aiohttp` session, fans out requests under your
concurrency limit, follows links recursively, parses items, and calls
`save()` on each one.

## Optional: use XPath instead of CSS

```python
from gain import Item, XPathParser, Xpath


class Post(Item):
    title = Xpath('//h1[@class="title"]/text()')


parsers = [
    XPathParser('//a[contains(@class, "next-page")]/@href'),
    XPathParser('//a[@class="post-link"]/@href', Post),
]
```

## Optional: speed up with uvloop (Linux)

```bash
pip install "gain[uvloop]"
```

`gain` will auto-detect and switch event loop policies — no code change
needed.
