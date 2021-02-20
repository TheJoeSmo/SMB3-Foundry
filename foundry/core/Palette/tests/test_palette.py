

from foundry.core.Color.Color import Color
from foundry.core.Palette.Palette import Palette


def test_initialization():
    Palette(Color(0, 0, 0), Color(0, 0, 0), Color(0, 0, 0), Color(0, 0, 0))


def test_colors():
    p = Palette(Color(0, 0, 0), Color(1, 1, 1), Color(2, 2, 2), Color(3, 3, 3))
    assert p[0].red == 0
    assert p[1].red == 1
    assert p[2].red == 2
    assert p[3].red == 3
