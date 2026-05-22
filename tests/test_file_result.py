import os

import pytest

from gain.result import FileResult


@pytest.mark.asyncio
async def test_file_result_saves_string_to_disk(tmp_path):
    target = tmp_path / "spider.data"
    result = FileResult(f"file:///{target}")

    await result.save("test_str")

    assert target.read_text() == "test_str\n"


@pytest.mark.asyncio
async def test_file_result_rejects_non_file_scheme():
    with pytest.raises(ValueError):
        FileResult("http://example.com/foo")


def test_file_result_cleans_up_legacy_artifact():
    legacy = "spider.data"
    if os.path.exists(legacy):
        os.remove(legacy)
    assert not os.path.exists(legacy)
