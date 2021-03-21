

from typing import Optional
from PySide2.QtWidgets import QWidget

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Size.Size import Size

from foundry.gui.Block.TileSquareAssemblyDisplayer import TileSquareAssemblyDisplayer
from foundry.gui.Block.TrackingBlock import TrackingBlock
from foundry.gui.Block.Block import Block


class TileSquareAssemblyPicker(TileSquareAssemblyDisplayer):
    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Tile Square Assembly Picker</b><br>Click a block to select it<br/>"

    def __init__(
            self,
            parent: Optional[QWidget],
            palette_set: PaletteSet,
            tileset: int,
            size: Optional[Size] = None
    ) -> None:
        self.block_selected_update_observable = GenericObservable("block_selected_update")

        super().__init__(parent, palette_set, tileset, size)

    def _load_block(self, idx: int) -> QWidget:
        widget = TrackingBlock(
            self,
            Block.from_tsa(self.block_size, idx, self.pattern_table, self.palette_set, self.tileset)
        )

        self.palette_set_update_observable.attach_observer(lambda pal: setattr(widget, "palette_set", pal))

        def set_pattern_table(pattern_table: PatternTable):
            widget.pattern_table.pattern_table = pattern_table

        self.pattern_table_update_observable.attach_observer(set_pattern_table)

        widget.single_click_observable.attach_observer(
            lambda *_, i=idx: self.block_selected_update_observable.notify_observers(i)
        )
        return widget
