# Result backends

A *result backend* persists parsed items without you having to override
`Item.save()`. `gain` ships with one production backend (`FileResult`) and
a stub for MySQL.

## Attaching a backend

```python
from gain import Item, Css
from gain.result import FileResult


class Post(Item):
    __result__ = FileResult("file:///posts.txt")
    title = Css(".entry-title")
```

With `__result__` set, `Item.save()` forwards `self.results` to the
backend's `.save()`. You don't need to override anything.

## `FileResult(url)`

Appends each item's results (one record per line) to a local file. `url`
must start with `file:///` — the path follows.

```python
FileResult("file:///tmp/posts.txt")
```

The file is opened in append mode each time, so multiple parses across
multiple runs accumulate. Delete the file between runs if you want a fresh
batch.

## `MySQLResult(url)`

Stub backend — does nothing yet. Reserved for future use.

## Writing your own

Subclass `gain.result.base.BaseResult` and implement `prepare()`,
`save(self, results)`, and `format_result(self, result)`. The URL passed to
the constructor is parsed RFC-1738 style; the fields end up on `self` as
`schema`, `username`, `password`, `host`, `port`, `database`.
