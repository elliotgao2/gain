# coding: utf-8
# /usr/bin/env python3
# author: c1ay
# email: liukaiash@gmail.com
import aiofiles

from .base import BaseResult


class FileResult(BaseResult):

    def __init__(self, url, **kwargs):
        super().__init__(url)
        if self.schema != 'file':
            raise ValueError('scheme error')
        self.path = self.database

    def prepare(self):
        """
        check file exist
        :return:
        """
        pass

    async def save(self, results):
        results = self.format_result(results)
        await self.save_to_file(results)

    def format_result(self, result):
        return str(result) + "\n"

    async def save_to_file(self, results):
        """
        save results to file Asynchronous
        :param results: str
        :return: None
        """
        async with aiofiles.open(self.path, 'a+') as f:
            await f.write(results)
