import os
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


def test_get_terminal_size():
    _, fd = os.openpty()
    width, height = core.get_terminal_size(fd)
    assert width == 0
    assert height == 0


class TestImageRow:
    def test_image_size(self, testdata: Path):
        row = core.ImageRow(box_width=200, box_height=220, padding=5, bg_color="black")
        row.add(testdata / "coffee.jpg")
        row.add(testdata / "sea.png")
        img = row.to_image()

        assert img.width == 400
        assert img.height == 220
