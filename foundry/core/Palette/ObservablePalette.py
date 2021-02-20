

from ..Observables.GenericObservable import GenericObservable
from ..Color.Color import Color
from ..Color.ObservableColor import ObservableColor
from Palette import Palette


def _get_color(palette: Palette, index: int) -> ObservableColor:
    return palette[index]


def _set_color(palette: Palette, index: int, color: Color):
    palette[index] = color


class ObservablePalette(Palette):
    """
    A palette that emits an update when edited
    """

    def __init__(self, color_0: Color, color_1: Color, color_2: Color, color_3: Color):
        self._palette = Palette(
            ObservableColor.from_color(color_0),
            ObservableColor.from_color(color_1),
            ObservableColor.from_color(color_2),
            ObservableColor.from_color(color_3)
        )
        self.update_action = GenericObservable("palette_update")

    def __str__(self) -> str:
        return self._palette.__str__()

    def __getitem__(self, item: int) -> Color:
        #  We provide ObservableColors to the actual palette, which will be returned
        #  This provides an entire copy, to protect the palette from any external changes
        return self._palette[item].color

    def __setitem__(self, key: int, value: Color):
        pal = self.palette  # This is a copy of the actual palette being edited
        pal[key] = ObservableColor.from_color(value)
        self.palette = pal

    @property
    def nes_str(self) -> str:
        """Returns the color as a NES string"""
        return self._palette.nes_str

    @property
    def color_0(self) -> Color:
        return _get_color(self, 0).color

    @color_0.setter
    def color_0(self, color: Color):
        _set_color(self, 0, color)

    @property
    def color_1(self) -> Color:
        return _get_color(self, 1).color

    @color_1.setter
    def color_1(self, color: Color):
        _set_color(self, 1, color)

    @property
    def color_2(self) -> Color:
        return _get_color(self, 2).color

    @color_2.setter
    def color_2(self, color: Color):
        _set_color(self, 2, color)

    @property
    def color_3(self) -> Color:
        return _get_color(self, 3).color

    @color_3.setter
    def color_3(self, color: Color):
        _set_color(self, 3, color)

    @property
    def palette(self) -> Palette:
        """
        This provides a full copy of the palette.  Even the colors will not refer to the actual palette.
        :return:
        """
        return Palette(self._palette[0], self._palette[1], self._palette[2], self._palette[3])

    @palette.setter
    def palette(self, palette: Palette) -> None:
        self._palette = palette
        self.update_action(palette)
