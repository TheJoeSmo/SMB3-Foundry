

from typing import Optional
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Size.Size import Size
from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.core.Block.AbstractBlock import AbstractBlock
from foundry.core.Block.Block import Block
from foundry.gui.Block.ObservableBlock import ObservableBlock
from foundry.gui.Tile.Tile import Tile
from foundry.gui.Tile.WidgetTile import WidgetTile


class BlockTileDisplayer(QWidget):
    """A class for displaying a Block as four smaller Tiles"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Block Tile Displayer</b><br>Displays a block as four smaller tiles<br/>"

    def __init__(self, parent: Optional[QWidget], block: AbstractBlock) -> None:
        super().__init__(parent)

        self.update_observable = GenericObservable("update")
        self.update_observable.attach_observer(lambda *_: self.update())

        self._block = ObservableBlock.from_block(block)
        self._block.update_observable.attach_observer(self.update_observable.notify_observers)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for idx in range(4):
            grid.addWidget(self._create_tile(idx, self._block.tiles[idx]), idx & 1, idx // 2)

        self.setLayout(grid)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    def _create_tile(self, idx: int, tile_idx: int) -> QWidget:
        widget = WidgetTile(
            self,
            Tile(self._block.size, tile_idx, self._block.pattern_table, self._block.palette_set[tile_idx // 0x40])
        )

        self._attach_observers_to_tile(widget, idx)

        return widget

    def _attach_observers_to_tile(self, widget: WidgetTile, idx: int):
        # Updates for the tile from the block upstream
        def update_tile_size(size: Size):
            widget.size = size

        self._block.size_update_observable.attach_observer(update_tile_size)

        def update_tile_index(*args):
            widget.index = self._block.tiles[idx]

        self._block.index_update_observable.attach_observer(update_tile_index)
        self._block.tsa_data_update_observable.attach_observer(lambda *_: update_tile_index(self._block.index))

        def update_pattern_table(pattern_table: PatternTable):
            widget.pattern_table.pattern_table = pattern_table

        self._block.pattern_table_update_observable.attach_observer(update_pattern_table)

        def update_palette_set(palette_set: PaletteSet):
            widget.palette = palette_set[self._block.index // 0x40]

        self._block.palette_set_update_observable.attach_observer(update_palette_set)

    @property
    def block(self) -> Block:
        return self._block.observed_block

    @block.setter
    def block(self, block: AbstractBlock) -> None:
        self._block.observed_block = block
