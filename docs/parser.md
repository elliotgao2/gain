# Parser

A `Parser` describes how to find URLs on a page. Two flavors:

- **Follow parser** — one argument. Matches URLs and queues them for
  further parsing.
- **Extract parser** — two arguments. Matches URLs, fetches each one, and
  instantiates an `Item` from the response.

```python
from gain import Parser

# Follow every page of pagination
Parser(r"https://blog.scrapinghub.com/page/\d+/")

# Extract a Post from every dated permalink
Parser(r"https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/", Post)
```

## `Parser(rule, item=None)`

- **`rule`** — a regular expression matched against the rendered HTML to
  pull out hrefs.
- **`item`** — optional. An `Item` subclass. When set, every matched URL is
  fetched and parsed as that item; when omitted, the URL is queued for
  another parser to handle.

## `XPathParser(rule, item=None)`

Same as `Parser`, but `rule` is an XPath expression evaluated against the
parsed DOM:

```python
from gain import XPathParser

XPathParser('//a[contains(@class, "next-page")]/@href')
XPathParser('//a[@class="post-link"]/@href', Post)
```

XPath is a better fit when the URLs you want are identified by
relationships in the DOM rather than by regex shape.

## URL normalization

Both parser types automatically:

- HTML-unescape matched URLs (`&amp;` → `&`).
- Resolve relative URLs against `Spider.base_url`.
- Deduplicate — each URL is parsed at most once per spider run.
