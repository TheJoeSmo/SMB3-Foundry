

from abc import abstractmethod
from typing import Optional
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPaintEvent, QPainter

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Position.Position import Position
from foundry.core.Size.Size import Size

from foundry.game.gfx.drawable.Block import Block

from foundry.gui.Block.AbstractBlock import AbstractBlock


class WidgetBlock(QWidget):
    """A class for keeping track of a Block"""
    def __init__(
            self,
            parent: Optional[QWidget],
            block: AbstractBlock,
            *args,
            **kwargs
    ) -> None:
        super().__init__(parent)
        self.block = block

        self.refresh_observable = GenericObservable("refresh")
        self.tile_update_observable = GenericObservable("tile_update")
        self.size_update_observable = GenericObservable("size_update")
        self.size_update_action.observer.attach_observer(self.refresh_event_action)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    @property
    def size(self) -> Size:
        """The size of the block in units of 16 pixels"""
        return self.block.size

    @size.setter
    def size(self, size: Size) -> None:
        self.block.size = size
        self.size_update_action(self.size)

    @property
    def index(self) -> int:
        """The index of the block"""
        return self.block.index

    @index.setter
    def index(self, index: int) -> None:
        self.block.index = index
        self.refresh_event_action()

    @property
    def tsa_data(self) -> bytearray:
        """Find the tsa data from a given offset"""
        return self.block.tsa_data

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        self.block.tsa_data = tsa_data
        self.refresh_event_action()

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self.block.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self.block.pattern_table = pattern_table
        self.refresh_event_action()

    @property
    def palette_set(self) -> PaletteSet:
        """The palette currently used by the tsa"""
        return self.block.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self.block.palette_set = palette_set
        self.refresh_event_action()

    def sizeHint(self):
        """The ideal size of the widget"""
        return QSize(16 * self.size.width, 16 * self.size.height)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paints the widget"""
        painter = QPainter(self)
        self.tile.draw(painter, Position(0, 0))
        super().paintEvent(event)