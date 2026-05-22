# Item

An `Item` is a data shape. You declare what fields you want and how to
find them; `gain` does the rest.

```python
from gain import Css, Item, Xpath


class Post(Item):
    title = Css(".entry-title")
    author = Xpath('//meta[@name="author"]/@content')

    async def save(self):
        print(self.results)
```

Each class attribute that is a selector becomes a field. Everything else
stays a regular class attribute or method.

## `save(self)`

Your async hook for persistence. Called once per parsed item. The parsed
field values are available on `self.results` (and as attributes:
`self.title`, `self.author`, ...).

```python
import aiofiles


class Post(Item):
    title = Css(".entry-title")

    async def save(self):
        async with aiofiles.open("posts.txt", "a+") as f:
            await f.write(self.title + "\n")
```

## Built-in result backends

For common destinations there's `gain.result.FileResult` (and a stub
`MySQLResult`). Attach one via `__result__`:

```python
from gain.result import FileResult


class Post(Item):
    __result__ = FileResult("file:///posts.txt")
    title = Css(".entry-title")
```

With `__result__` set, the default `save()` writes `self.results` through
the backend — you don't have to define `save()` yourself.

## `Item.count`

Class attribute. Incremented every time an instance is parsed
successfully. Available on the class object after the spider runs.
