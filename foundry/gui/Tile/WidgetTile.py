

from typing import Optional
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPaintEvent, QPainter

from foundry.core.util.update_types import \
    SIZE_UPDATE, REFRESH_UPDATE, INDEX_UPDATE, PALETTE_UPDATE, PATTERN_TABLE_UPDATE
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Palette.Palette import Palette
from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Position.Position import Position
from foundry.core.Size.Size import Size

from foundry.gui.Tile.AbstractTile import AbstractTile


class WidgetTile(QWidget):
    """A class for keeping track of a Tile"""
    def __init__(
            self,
            parent: Optional[QWidget],
            tile: AbstractTile,
            *args,
            **kwargs
    ) -> None:
        super().__init__(parent)
        self.tile = tile

        self.update_observable = GenericObservable("update")
        # Send a refresh update if needed
        self.update_observable.attach_observer(
            lambda update_type, *_: self.update_observable.notify_observers(REFRESH_UPDATE) if update_type > 1 else 0
        )
        # Redraw if a refresh update occurs
        self.update_observable.attach_observer(
            lambda update_type, *_: self.update() if update_type == 1 else 0
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.tile})"

    @property
    def index(self) -> int:
        """The index the tile is located in for the tsa"""
        return self.tile.index

    @index.setter
    def index(self, index: int) -> None:
        self.tile.index = index
        self.update_observable.notify_observers(INDEX_UPDATE, self.index)

    @property
    def size(self) -> Size:
        """The size of the tile in units of 8 pixels"""
        return self.tile.size

    @size.setter
    def size(self, size: Size) -> None:
        self.tile.size = size
        self.update_observable.notify_observers(SIZE_UPDATE, self.index)

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self.tile.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self.tile.pattern_table = pattern_table
        self.update_observable.notify_observers(PATTERN_TABLE_UPDATE, self.pattern_table)

    @property
    def palette(self) -> Palette:
        """The palette currently used"""
        return self.tile.palette

    @palette.setter
    def palette(self, palette: Palette) -> None:
        self.tile.palette = palette
        self.update_observable.notify_observers(PALETTE_UPDATE, self.pattern_table)

    def sizeHint(self):
        """The ideal size of the widget"""
        return QSize(8 * self.size.width, 8 * self.size.height)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paints the widget"""
        painter = QPainter(self)
        self.tile.draw(painter, Position(0, 0))
        super().paintEvent(event)
