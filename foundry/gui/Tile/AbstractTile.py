

from abc import abstractmethod
from typing import Optional
from PySide2.QtGui import QPainter

from foundry.game.gfx.drawable.Tile import Tile

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Palette.Palette import Palette
from foundry.core.Size.Size import Size
from foundry.core.Position.Position import Position


class AbstractTile:
    """The abstract representation of a tile"""
    def __init__(
            self,
            size: Optional[Size],
            index: int,
            ptn_tbl: PatternTableHandler,
            pallet: Palette,
            transparency: bool = True
    ) -> None:
        self._size = size
        self._index = index
        self._pattern_table = ptn_tbl
        self._palette = pallet
        self._transparency = transparency

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.size}, {self.index}, {self.pattern_table}, " \
               f"{self.palette}, {self.transparency})"

    @property
    @abstractmethod
    def size(self) -> Size:
        """The size of the tile in units of 8 pixels"""

    @size.setter
    @abstractmethod
    def size(self, size: Size) -> None:
        """"""

    @property
    @abstractmethod
    def index(self) -> int:
        """The index of the tile"""

    @index.setter
    def index(self, index: int) -> None:
        """"""

    @property
    @abstractmethod
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tile"""

    @pattern_table.setter
    @abstractmethod
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        """"""

    @property
    @abstractmethod
    def palette(self) -> Palette:
        """The palette currently used by tile"""

    @palette.setter
    @abstractmethod
    def palette(self, palette_set: Palette) -> None:
        """"""

    @property
    def tile(self) -> Tile:
        """The actual tile provided"""
        return Tile.from_palette(self.index, self.palette, self.pattern_table)

    def draw(self, painter: QPainter, position: Position, size: Optional[Size] = None):
        """Draws the tile to a given point"""
        size = size if size is not None else Size(self.size.width * 8, self.size.height * 8)
        self.tile.draw(painter, position.x, position.y, size.width)
