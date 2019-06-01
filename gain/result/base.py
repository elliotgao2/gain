# coding: utf-8
# /usr/bin/env python3
# author: c1ay liukaiash@gmail.com
import re


def _parse_rfc1738_args(url):
    pattern = re.compile(r'''
        (?P<name>[\w\+]+)://
        (?:
            (?P<username>[^:/]*)
            (?::(?P<password>.*))?
        @)?
        (?:
            (?:
                \[(?P<ipv6host>[^/]+)\] |
                (?P<ipv4host>[^/:]+)
            )?
            (?::(?P<port>[^/]*))?
        )?
        (?:/(?P<database>.*))?
        ''', re.X)
    m = pattern.match(url)
    if m is not None:
        components = m.groupdict()
        ipv6 = components.pop('ipv6host')
        ipv4 = components.pop('ipv4host')
        components['host'] = ipv4 or ipv6
        return components
    else:
        raise ValueError('wrong url format')


class BaseResult:

    def __init__(self, url):
        self.url = url
        self._parse_url()
        self.prepare()

    def _parse_url(self):
        configs = _parse_rfc1738_args(self.url)
        self.schema = configs['name']
        self.username = configs['username']
        self.password = configs['password']
        self.host = configs['host']
        if configs['port']:
            self.port = int(configs['port'])
        else:
            self.port = None
        self.database = configs['database']

    def prepare(self):
        """
        init config
        :return:
        """
        raise NotImplementedError

    async def save(self, results):
        raise NotImplementedError

    def format_result(self, result):
        raise NotImplementedError
