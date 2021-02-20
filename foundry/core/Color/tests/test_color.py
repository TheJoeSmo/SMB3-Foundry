

from foundry.core.Color.Color import Color


def test_init():
    Color(0, 0, 0)


def test_red():
    assert Color(1, 0, 0).red == 1


def test_green():
    assert Color(0, 1, 0).green == 1


def test_blue():
    assert Color(0, 0, 1).blue == 1
