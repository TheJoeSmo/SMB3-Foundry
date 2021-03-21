

from typing import Optional

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.PaletteSet.ObservablePaletteSet import ObservablePaletteSet
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

        self.update_observable = GenericObservable("update")
        self.update_observable.attach_observer(self.update)
        self.palette_set_update_observable = GenericObservable("palette_set_update")
        self.palette_set_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.pattern_table_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.tileset_update_observable = GenericObservable("tileset_update")

        def update_tileset(tileset):
            self.pattern_table.pattern_table = PatternTable.from_tileset(tileset)

        self.tileset_update_observable.attach_observer(update_tileset)
        self._palette_set = ObservablePaletteSet.from_palette_set(palette_set)
        self._pattern_table = PatternTableHandler(PatternTable.from_tileset(tileset))
        self._tileset = tileset
        self.block_size = size if size is not None else Size(1, 1)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        grid_layout.setDefaultPositioning(0x10, Qt.Horizontal)

        for idx in range(0x100):
            tile = self._load_block(idx)
            grid_layout.addWidget(tile, row=idx % 0x10, column=idx // 0x10)

        self.setLayout(grid_layout)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.palette_set},{self.tileset}, {self.block_size})"

    def _load_block(self, idx: int) -> QWidget:
        widget = WidgetBlock(
            self,
            Block.from_tsa(self.block_size, idx, self.pattern_table, self.palette_set, self.tileset)
        )
        self.palette_set_update_observable.attach_observer(lambda pal: setattr(widget, "palette_set", pal))

        def set_pattern_table(pattern_table: PatternTable):
            widget.pattern_table.pattern_table = pattern_table

        self.pattern_table_update_observable.attach_observer(set_pattern_table)

        return widget

    @property
    def palette_set(self) -> ObservablePaletteSet:
        return self._palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self._palette_set.palette_set = palette_set
        self.palette_set_update_observable.notify_observers(self.palette_set.palette_set)

    @property
    def pattern_table(self) -> PatternTableHandler:
        return self._pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTable) -> None:
        self._pattern_table.pattern_table = pattern_table
        self.pattern_table_update_observable.notify_observers(self.pattern_table.pattern_table)

    @property
    def tileset(self) -> int:
        return self._tileset

    @tileset.setter
    def tileset(self, tileset: int) -> None:
        self._tileset = tileset
        self.tileset_update_observable.notify_observers(tileset)
