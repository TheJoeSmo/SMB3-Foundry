

from PySide2.QtWidgets import QWidget

from foundry.gui.Block.BlockTileTracker import BlockTileTracker
from foundry.gui.Tile.TilePickerPopUp import TilePickerPopUp


class BlockTileEditor(BlockTileTracker):
    """A class for selecting tiles for a Block"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Block Tile Tracker</b><br>Tracks a block as four smaller tiles<br/>"

    def _create_tile(self, idx: int, tile_idx: int) -> QWidget:
        tile = super()._create_tile(idx, tile_idx)

        # On double click bring up a dialog to select a tile and on finish update the tile accordingly
        tile.double_click_observable.attach_observer(
            lambda *_: TilePickerPopUp(
                self,
                tile.tile_palette,
                self.block.pattern_table,
                self.block.size,
                action=lambda i, t=tile: setattr(t, "index", i)
            )
        )

        return tile
