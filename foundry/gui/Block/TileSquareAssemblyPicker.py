

from PySide2.QtWidgets import QWidget

from foundry.gui.Block.TileSquareAssemblyDisplayer import TileSquareAssemblyDisplayer
from foundry.gui.Block.TrackingBlock import TrackingBlock
from foundry.gui.Block.Block import Block


class TileSquareAssemblyPicker(TileSquareAssemblyDisplayer):
    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Tile Square Assembly Picker</b><br>Click a block to select it<br/>"

    def _load_block(self, idx: int) -> QWidget:
        widget = TrackingBlock(
            self,
            Block.from_tsa(self.block_size, idx, self.pattern_table, self.palette_set, self.tileset)
        )
        widget.single_click_observable.attach_observer(lambda *_, i=idx: self.update_action(i))
        return widget
