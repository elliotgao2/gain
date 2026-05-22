# Selectors

A selector pulls a field value out of an HTML page. Three flavors ship with
`gain`:

## `Css(rule, attr=None)`

CSS selector via `pyquery`. Returns the text of the first match by default;
pass `attr=` to read an attribute.

```python
from gain import Css

title = Css(".entry-title")
href = Css("a.permalink", attr="href")
```

## `Xpath(rule, attr=None)`

XPath via `lxml`.

```python
from gain import Xpath

title = Xpath('//h1[@class="title"]')
author = Xpath('//meta[@name="author"]/@content')
```

When the XPath matches a single node, the value is returned as a string.
When it matches multiple nodes, a list of strings is returned.

## `Regex(rule)`

Plain regex on the raw HTML. Returns the first match.

```python
from gain import Regex

post_id = Regex(r"post-id-(\d+)")
```

## Choosing a selector

- **CSS** — easiest to read, perfect for class/id-based extraction.
- **XPath** — needed when selecting by axis (parent, sibling) or by
  attribute predicates that CSS can't express.
- **Regex** — the escape hatch. Use when the data is embedded in inline
  JavaScript or doesn't have a clean DOM structure.

If a selector matches nothing, the field is silently omitted from
`self.results` and an error is logged. Wrap it in your own try/except
inside `save()` if you need to enforce presence.
