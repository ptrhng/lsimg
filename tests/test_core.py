from pathlib import Path

import pytest

from lsimg import core


def test_is_image_file_valid():
    names = {
        "cat.gif",
        "dog.jpeg",
    }
    for name in names:
        assert core.is_image_file(name)


def test_is_image_file_invalid():
    assert not core.is_image_file("noext")


@pytest.fixture
def testdata() -> Path:
    return Path(__file__).parent / "testdata"


def test_find_image_files_dir(testdata: Path):
    assert sorted(core.find_image_files(testdata)) == [
        testdata / "coffee.jpg",
        testdata / "sea.png",
        testdata / "spongebob.gif",
    ]


def test_find_iamge_files_single_file(testdata: Path):
    assert core.find_image_files(testdata / "coffee.jpg") == [testdata / "coffee.jpg"]


def test_find_image_files_ignore_nonexistent(testdata: Path):
    assert core.find_image_files(testdata / "nonexistent") == []
