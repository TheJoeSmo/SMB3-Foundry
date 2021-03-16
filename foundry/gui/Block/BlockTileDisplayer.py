

from typing import Optional
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.core.Observables.GenericObservable import GenericObservable

from foundry.gui.Block.AbstractBlock import AbstractBlock
from foundry.gui.Tile.Tile import Tile
from foundry.gui.Tile.WidgetTile import WidgetTile


class BlockTileDisplayer(QWidget):
    """A class for displaying a Block as four smaller Tiles"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Block Tile Displayer</b><br>Displays a block as four smaller tiles<br/>"

    def __init__(self, parent: Optional[QWidget], block: AbstractBlock) -> None:
        super().__init__(parent)
        self.block = block

        self.update_observable = GenericObservable("update")

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for idx in range(4):
            grid.addWidget(self._create_tile(self.block.tiles[idx]), idx & 1, idx // 2)

        self.setLayout(grid)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    def _create_tile(self, idx) -> QWidget:
        return WidgetTile(
            self,
            Tile(self.block.size, idx, self.block.pattern_table, self.block.palette_set[idx // 0x40])
        )
