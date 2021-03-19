

from typing import Optional
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPaintEvent, QPainter

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

        # Connect observables
        self.update_observable = GenericObservable("update")
        self.update_observable.attach_observer(lambda *_: self.update())
        self.index_update_observable = GenericObservable("index_update")
        self.index_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.size_update_observable = GenericObservable("size_update")
        self.size_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.pattern_table_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.palette_update_observable = GenericObservable("palette_update")
        self.palette_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.tile})"

    @property
    def index(self) -> int:
        """The index the tile is located in for the tsa"""
        return self.tile.index

    @index.setter
    def index(self, index: int) -> None:
        self.tile.index = index
        self.index_update_observable.notify_observers(index)

    @property
    def size(self) -> Size:
        """The size of the tile in units of 8 pixels"""
        return self.tile.size

    @size.setter
    def size(self, size: Size) -> None:
        self.tile.size = size
        self.size_update_observable.notify_observers(size)

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self.tile.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self.tile.pattern_table = pattern_table
        self.pattern_table_update_observable.notify_observers(pattern_table)

    @property
    def palette(self) -> Palette:
        """The palette currently used"""
        return self.tile.palette

    @palette.setter
    def palette(self, palette: Palette) -> None:
        self.tile.palette = palette
        self.palette_update_observable.notify_observers(palette)

    def sizeHint(self):
        """The ideal size of the widget"""
        return QSize(8 * self.size.width, 8 * self.size.height)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paints the widget"""
        painter = QPainter(self)
        self.tile.draw(painter, Position(0, 0))
        super().paintEvent(event)
