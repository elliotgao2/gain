import os
import sys
sys.path.append('..')
from gain.result import FileResult
import asyncio


def test_file_result():
    test_file = "spider.data"
    url = "file:///{}".format(test_file)
    f = FileResult(url)
    test_str = "test_str"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(f.save(test_str))

    with open(test_file, 'r+') as file_to_test:
        assert file_to_test.read() == test_str + "\n"
        
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == "__main__":
    test_file_result()
