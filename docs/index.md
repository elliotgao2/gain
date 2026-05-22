# gain

> Async web crawling framework for everyone.

`gain` is a tiny crawling framework built on `asyncio`, `aiohttp`, and
`lxml`/`pyquery`. You declare items and parsers; `gain` handles the
concurrency, retries, and persistence.

## A 20-line example

```python
import aiofiles
from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css(".entry-title")

    async def save(self):
        async with aiofiles.open("posts.txt", "a+") as f:
            await f.write(self.results["title"] + "\n")


class MySpider(Spider):
    concurrency = 5
    start_url = "https://blog.scrapinghub.com/"
    parsers = [
        Parser(r"https://blog.scrapinghub.com/page/\d+/"),
        Parser(r"https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/", Post),
    ]


MySpider.run()
```

## How it works

1. **Spider** kicks off from `start_url` under a concurrency budget.
2. **Parsers** either *follow* (one argument) — discovering more URLs to
   queue — or *extract* (two arguments) — instantiating an `Item` from each
   matching page.
3. **Items** use `Css` / `Xpath` / `Regex` selectors to pull fields out of
   HTML.
4. **`save()`** is your async hook to persist results.

## Next steps

- [Tutorial](tutorial.md) — a full walk-through.
- [Spider](spider.md) — the top-level orchestrator.
- [Parser](parser.md) — following vs extracting.
- [Item](item.md) — declaring data shapes.
- [Selectors](selector.md) — picking values out of HTML.
- [Result](result.md) — persisting parsed items.
