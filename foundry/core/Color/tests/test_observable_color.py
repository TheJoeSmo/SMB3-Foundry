

from foundry.core.Color.ObservableColor import ObservableColor as Color


def test_init():
    Color(0, 0, 0)


def test_red():
    assert Color(1, 0, 0).red == 1


def test_green():
    assert Color(0, 1, 0).green == 1


def test_blue():
    assert Color(0, 0, 1).blue == 1


def test_functional_implementation_of_color():
    color = Color(0, 1, 2)
    real_color = color._color  # The real color
    color.color = Color(2, 1, 0)
    assert color._color is not real_color  # They should be different instances
    assert color._color is not color.color


def test_functional_implementation_of_red():
    color = Color(0, 0, 0)
    real_color = color.from_color
    color.red = 1
    assert color._color is not real_color


def test_functional_implementation_of_green():
    color = Color(0, 0, 0)
    real_color = color.from_color
    color.green = 1
    assert color._color is not real_color


def test_functional_implementation_of_blue():
    color = Color(0, 0, 0)
    real_color = color.from_color
    color.blue = 1
    assert color._color is not real_color

