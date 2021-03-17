

from PySide2.QtWidgets import QWidget

from foundry.gui.Block.BlockTileDisplayer import BlockTileDisplayer
from foundry.gui.Tile.TrackingTile import TrackingTile
from foundry.gui.Tile.Tile import Tile


class BlockTileTracker(BlockTileDisplayer):
    """A class for selecting tiles for a Block"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Block Tile Tracker</b><br>Tracks a block as four smaller tiles<br/>"

    def _create_tile(self, idx: int, tile_idx: int) -> QWidget:
        tile = TrackingTile(
            self,
            Tile(self.block.size, tile_idx, self.block.pattern_table, self.block.palette_set[tile_idx // 0x40])
        )

        # Push the tile update upstream

        def push_tile_to_block(tile_index, i):
            tile = list(self.block.tiles)
            tile[i] = tile_index
            self.block.tiles = tuple(tile)

        tile.index_update_observable.attach_observer(lambda tile_index, i=idx: push_tile_to_block(tile_index, i))

        return tile