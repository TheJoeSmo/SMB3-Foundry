

from typing import Optional

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Palette.Palette import Palette
from foundry.core.Size.Size import Size

from foundry.gui.Tile.WidgetTile import WidgetTile
from foundry.gui.Tile.Tile import Tile


class PatternTableDisplayer(QWidget):
    """A widget that shows all the tiles of a pattern table"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Pattern Table Displayer</b><br>Displays all the tiles in a pattern table<br/>"

    def __init__(
            self,
            parent: Optional[QWidget],
            palette: Palette,
            pattern_table: PatternTableHandler,
            size: Optional[Size] = None
    ) -> None:
        super().__init__(parent)
        self.tile_palette = palette
        self.pattern_table = pattern_table
        self.tile_size = size if size is not None else Size(1, 1)

        self.update_observable = GenericObservable("update")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        grid_layout.setDefaultPositioning(0x10, Qt.Horizontal)

        for idx in range(0x100):
            tile = self._load_tile(idx)
            grid_layout.addWidget(tile, row=idx % 0x10, column=idx // 0x10)

        self.setLayout(grid_layout)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.tile_palette},{self.pattern_table}, {self.tile_size})"

    def _load_tile(self, idx: int) -> QWidget:
        return WidgetTile(self, Tile(self.tile_size, idx, self.pattern_table, self.tile_palette))
