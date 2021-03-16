

from typing import Optional

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Size.Size import Size

from foundry.gui.Block.WidgetBlock import WidgetBlock
from foundry.gui.Block.Block import Block


class TileSquareAssemblyDisplayer(QWidget):
    """A widget that shows all the blocks in a tileset"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Tile Square Assembly Displayer</b><br>Displays all the blocks in a given tileset<br/>"

    def __init__(
            self,
            parent: Optional[QWidget],
            palette_set: PaletteSet,
            tileset: int,
            size: Optional[Size] = None
    ) -> None:
        super().__init__(parent)
        self.tile_palette = palette_set
        self.tileset = tileset
        self.tile_size = size if size is not None else Size(1, 1)

        self.update_observable = GenericObservable("update")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        grid_layout.setDefaultPositioning(0x10, Qt.Horizontal)

        for idx in range(0x100):
            tile = self._load_block(idx)
            grid_layout.addWidget(tile, row=idx % 0x10, column=idx // 0x10)

        self.setLayout(grid_layout)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.tile_palette},{self.tileset}, {self.tile_size})"

    def _load_block(self, idx: int) -> QWidget:
        return WidgetBlock(
            self,
            Block.from_tsa(self.block_size, idx, self.pattern_table, self.palette_set, self.tileset)
        )

    @property
    def tileset(self) -> int:
        return self._tileset

    @tileset.setter
    def tileset(self, tileset: int) -> None:
        self._tileset = tileset
        self.pattern_table = PatternTableHandler.from_tileset(tileset)
