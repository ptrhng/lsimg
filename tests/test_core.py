from lsimg import core


def test_is_image_file_valid():
    names = {'cat.gif', 'dog.jpeg',}
    for name in names:
        assert core.is_image_file(name)


def test_is_image_file_invalid():
    assert not core.is_image_file('noext')
