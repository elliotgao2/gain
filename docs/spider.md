# Spider

`Spider` is the top-level orchestrator. Subclass it, set a few class
attributes, and call `Spider.run()`.

```python
from gain import Parser, Spider


class MySpider(Spider):
    start_url = "https://blog.scrapinghub.com/"
    concurrency = 5
    headers = {"User-Agent": "Google Spider"}
    parsers = [Parser(r"https://blog.scrapinghub.com/page/\d+/")]


MySpider.run()
```

## Class attributes

| Attribute      | Default | Description                                       |
| -------------- | ------- | ------------------------------------------------- |
| `start_url`    | `""`    | The seed URL `gain` fetches first.                |
| `base_url`     | `None`  | Override the derived base URL for relative links. |
| `parsers`      | `[]`    | List of `Parser` / `XPathParser` instances.       |
| `concurrency`  | `5`     | Maximum in-flight requests at any moment.         |
| `headers`      | `{}`    | Dict, or a callable returning a dict.             |
| `proxy`        | `None`  | HTTP/HTTPS proxy URL passed to `aiohttp`.         |
| `cookie_jar`   | `None`  | An `aiohttp.CookieJar` to share across requests.  |

## `Spider.run()`

Starts the event loop, fetches `start_url`, dispatches to every parser, and
blocks until the URL queue drains. Catches `KeyboardInterrupt` cleanly.

## Lifecycle

1. `start_url` is fetched once.
2. Each `Parser` extracts URLs and enqueues them.
3. Workers (one per parser, up to `concurrency`) drain the queue, fetching
   pages and either following them or extracting items.
4. When every queue is empty and no requests are in flight, the spider
   exits and prints a summary (item counts, request count, error count,
   elapsed time).
