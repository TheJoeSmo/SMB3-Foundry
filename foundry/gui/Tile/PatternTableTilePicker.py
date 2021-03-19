

from PySide2.QtWidgets import QWidget

from foundry.gui.Tile.PatternTableDisplayer import PatternTableDisplayer
from foundry.gui.Tile.TrackingTile import TrackingTile

from foundry.gui.Tile.Tile import Tile


class PatternTableTilePicker(PatternTableDisplayer):

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Pattern Table Tile Picker</b><br>Click a tile to select it<br/>"

    def _load_tile(self, idx: int) -> QWidget:
        widget = TrackingTile(self, Tile(self.tile_size, idx, self.pattern_table, self.tile_palette))
        widget.single_click_observable.attach_observer(lambda *_, i=idx: self.update_observable(i))
        return widget
