

from typing import Optional
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPaintEvent, QPainter

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Position.Position import Position
from foundry.core.Size.Size import Size

from foundry.gui.Block.ObservableBlock import ObservableBlock
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
        self.block = ObservableBlock.from_block(block)

        self.update_observable = GenericObservable("update")
        self.update_observable.attach_observer(lambda *_: self.update())
        self.block.update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    @property
    def size(self) -> Size:
        """The size of the block in units of 16 pixels"""
        return self.block.size

    @size.setter
    def size(self, size: Size) -> None:
        self.block.size = size

    @property
    def index(self) -> int:
        """The index of the block"""
        return self.block.index

    @index.setter
    def index(self, index: int) -> None:
        self.block.index = index

    @property
    def tsa_data(self) -> bytearray:
        """Find the tsa data from a given offset"""
        return self.block.tsa_data

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        self.block.tsa_data = tsa_data

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self.block.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self.block.pattern_table = pattern_table

    @property
    def palette_set(self) -> PaletteSet:
        """The palette currently used by the tsa"""
        return self.block.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self.block.palette_set = palette_set

    def sizeHint(self):
        """The ideal size of the widget"""
        return QSize(16 * self.size.width, 16 * self.size.height)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paints the widget"""
        painter = QPainter(self)
        self.tile.draw(painter, Position(0, 0))
        super().paintEvent(event)
