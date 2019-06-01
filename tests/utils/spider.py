from gain import Spider
from aiocache import caches
from aiocache import SimpleMemoryCache

cache = SimpleMemoryCache()

class FakeCacheSpider:
    proxy = None
    cache_enabled = True
    cache_alias = Spider.cache_alias
    cache_config = Spider.cache_config
    caches = None
    headers = None
    cache_disabled_urls = ["http://localhost:8080/calls"]

    def __init__(self):
        if caches and not self.caches:
            if self.cache_enabled and self.cache_config:
                caches.set_config(self.cache_config)
                self.caches = caches
