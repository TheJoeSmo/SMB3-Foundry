

from typing import Union

from ..Observables.GenericObservable import GenericObservable
from ..Palette.Palette import Palette
from ..Palette.ObservablePalette import ObservablePalette
from PaletteSet import PaletteSet


def _get_palette(palette_set: Union[PaletteSet, "ObservablePaletteSet"], index: int) -> ObservablePalette:
    return palette_set[index]


def _set_palette(palette_set: Union[PaletteSet, "ObservablePaletteSet"], index: int, palette: Palette):
    palette_set[index] = palette


class ObservablePaletteSet(Palette):
    """
    A palette that emits an update when edited
    """

    def __init__(self, palette_0: Palette, palette_1: Palette, palette_2: Palette, palette_3: Palette):
        self._palette_set = PaletteSet(
            ObservablePalette.from_palette(palette_0),
            ObservablePalette.from_palette(palette_1),
            ObservablePalette.from_palette(palette_2),
            ObservablePalette.from_palette(palette_3)
        )
        self.update_action = GenericObservable("palette_update")

    def __str__(self) -> str:
        return self._palette.__str__()

    def __getitem__(self, item: int) -> Palette:
        #  We provide ObservablePalette to the actual palette set, which will be returned
        #  This provides an entire copy, to protect the palette set from any external changes
        return self._palette_set[item].palette

    def __setitem__(self, key: int, value: Palette):
        pal = self.palette  # This is a copy of the actual palette being edited
        pal[key] = ObservablePalette.from_palette(value)
        self.palette_set = pal

    @classmethod
    def from_palette(cls, palette_set: PaletteSet):
        """Generates a ObservableColor from a color"""
        return cls(palette_set.palette_0, palette_set.palette_1, palette_set.palette_2, palette_set.palette_3)

    @property
    def nes_str(self) -> str:
        """Returns the color as a NES string"""
        return self._palette_set.nes_str

    @property
    def palette_0(self) -> Palette:
        return _get_palette(self, 0).palette

    @palette_0.setter
    def palette_0(self, palette: Palette):
        _set_palette(self, 0, palette)

    @property
    def palette_1(self) -> Palette:
        return _get_palette(self, 1).palette

    @palette_1.setter
    def palette_1(self, palette: Palette):
        _set_palette(self, 1, palette)

    @property
    def palette_2(self) -> Palette:
        return _get_palette(self, 2).palette

    @palette_2.setter
    def palette_2(self, palette: Palette):
        _set_palette(self, 2, palette)

    @property
    def palette_3(self) -> Palette:
        return _get_palette(self, 3).palette

    @palette_3.setter
    def palette_3(self, palette: Palette):
        _set_palette(self, 3, palette)

    @property
    def palette_set(self) -> PaletteSet:
        """
        This provides a full copy of the palette set.  Even the colors will not refer to the actual palette.
        """
        return PaletteSet(self._palette_set[0], self._palette_set[1], self._palette_set[2], self._palette_set[3])

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self._palette_set = palette_set
        self.update_action(palette_set)
