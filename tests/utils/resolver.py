
import socket
from aiohttp.resolver import DefaultResolver


class FakeResolver:
    _LOCAL_HOST = {0: '127.0.0.1',
                   socket.AF_INET: '127.0.0.1',
                   socket.AF_INET6: '::1'}

    def __init__(self, fakes, *, loop):
        """fakes -- dns -> port dict"""
        self._fakes = fakes
        self._resolver = DefaultResolver(loop=loop)

    async def resolve(self, host, port=0, family=socket.AF_INET):
        fake_port = self._fakes.get(host)
        if fake_port is not None:
            return [{'hostname': host,
                     'host': self._LOCAL_HOST[family], 'port': fake_port,
                     'family': family, 'proto': 0,
                     'flags': socket.AI_NUMERICHOST}]
        else:
            return await self._resolver.resolve(host, port, family)