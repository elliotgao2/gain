# coding: utf-8
# /usr/bin/env python3
# author: c1ay
# email: liukaiash@gmail.com
from .base import BaseResult


class MySQLResult(BaseResult):

    def __init__(self, url):
        super().__init__(url)

    def perpare(self):
        """
        init mysql table
        :return:
        """
        pass

    async def save(self, results):
        pass
