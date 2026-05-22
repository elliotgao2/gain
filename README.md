# gain

[![CI](https://img.shields.io/github/actions/workflow/status/elliotgao2/gain/ci.yml?branch=master&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/elliotgao2/gain/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/gain?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=3775A9)](https://pypi.org/project/gain/)
[![Python](https://img.shields.io/pypi/pyversions/gain?style=for-the-badge&logo=python&logoColor=white&color=3776AB)](https://pypi.org/project/gain/)
[![License](https://img.shields.io/pypi/l/gain?style=for-the-badge&color=A31F34)](https://pypi.org/project/gain/)
[![Downloads](https://img.shields.io/pypi/dm/gain?style=for-the-badge&logo=pypi&logoColor=white&label=Downloads&color=5C7CFA)](https://pypi.org/project/gain/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=for-the-badge)](https://github.com/astral-sh/uv)

> Async web crawling framework for everyone.

Built on `asyncio`, `aiohttp`, and `lxml`/`pyquery`. Declare items and
parsers; `gain` handles the concurrency, retries, and persistence.

## Install

```bash
pip install gain
```

Linux users can opt into `uvloop` for an extra speed bump:

```bash
pip install "gain[uvloop]"
```

Requires Python 3.10+.

## Quickstart

```python
import aiofiles
from gain import Css, Item, Parser, Spider


class Post(Item):
    title = Css(".entry-title")
    content = Css(".entry-content")

    async def save(self):
        async with aiofiles.open("scrapinghub.txt", "a+") as f:
            await f.write(self.results["title"] + "\n")


class MySpider(Spider):
    concurrency = 5
    headers = {"User-Agent": "Google Spider"}
    start_url = "https://blog.scrapinghub.com/"
    parsers = [
        Parser(r"https://blog.scrapinghub.com/page/\d+/"),
        Parser(r"https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/", Post),
    ]


MySpider.run()
```

Run it:

```bash
python spider.py
```

### XPath parsers

```python
from gain import Css, Item, Parser, Spider, XPathParser


class Post(Item):
    title = Css(".breadcrumb_last")

    async def save(self):
        print(self.title)


class MySpider(Spider):
    start_url = "https://mydramatime.com/europe-and-us-drama/"
    concurrency = 5
    headers = {"User-Agent": "Google Spider"}
    parsers = [
        XPathParser('//span[@class="category-name"]/a/@href'),
        XPathParser('//div[contains(@class, "pagination")]/ul/li/a[contains(@href, "page")]/@href'),
        XPathParser('//div[@class="mini-left"]//div[contains(@class, "mini-title")]/a/@href', Post),
    ]
    proxy = "https://localhost:1234"


MySpider.run()
```

## How it works

```
   ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
   │  start_url │ ─▶ │  Parser    │ ─▶ │  Item      │ ─▶ │ save()     │
   │            │    │  (follow)  │    │  (extract) │    │  (persist) │
   └────────────┘    └────────────┘    └────────────┘    └────────────┘
                          ▲                                      │
                          └──────────── new urls ────────────────┘
```

1. **Spider** kicks off from `start_url` under a concurrency budget.
2. **Parsers** either *follow* (one argument) — discovering more URLs to
   queue — or *extract* (two arguments) — instantiating an `Item` from each
   matching page.
3. **Items** use `Css` / `Xpath` / `Regex` selectors to pull fields out of
   HTML.
4. **`save()`** is your async hook to persist results — write a file, push
   to a queue, insert into a database.

## Examples

See the [`example/`](example) directory for runnable scripts against
Scrapinghub, V2EX, and Sciencenet.

## Development

```bash
git clone https://github.com/elliotgao2/gain.git
cd gain
uv sync                 # install deps into .venv
uv run pytest           # run tests
uv run ruff check .     # lint
```

We use [uv](https://github.com/astral-sh/uv) for packaging and
[ruff](https://github.com/astral-sh/ruff) for lint + format. Install the
pre-commit hooks:

```bash
uv run pre-commit install
```

## Contributing

Pull requests are welcome. For non-trivial changes, please open an issue
first to discuss. Make sure `pytest` and `ruff check` pass before
submitting.

## License

[MIT](LICENSE) © Elliot Gao
