

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Palette.Palette import Palette
from foundry.core.Size.Size import Size

from .AbstractTile import AbstractTile


class Tile(AbstractTile):
    """A generic implementation of a Tile"""

    @property
    def size(self) -> Size:
        """The size of the tile in units of 8 pixels"""
        return self._size

    @size.setter
    def size(self, size: Size) -> None:
        self._size = size

    @property
    def index(self) -> int:
        """The index of the tile"""
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        self._index = index

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self._pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self._pattern_table = pattern_table

    @property
    def palette(self) -> Palette:
        """The palette currently used by the tsa"""
        return self._palette

    @palette.setter
    def palette(self, palette: Palette) -> None:
        self._palette = palette
