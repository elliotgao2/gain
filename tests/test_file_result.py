import sys
sys.path.append('..')
from gain.result import FileResult
import asyncio


def test_file_result():
    test_file = "spider.data"
    url = "file:///{}".format(test_file)
    f = FileResult(url)
    test_str = "test_str"
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(f.save(test_str))
    with open(test_file, 'r+') as test_file:
        assert test_file.read() == test_str + "\n"
