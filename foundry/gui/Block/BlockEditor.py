

from typing import Optional
from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtGui import Qt

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Size.Size import Size

from foundry.gui.Block.BlockTileEditor import BlockTileEditor
from foundry.gui.Block.ObservableBlock import ObservableBlock
from foundry.gui.Block.AbstractBlock import AbstractBlock
from foundry.gui.QSpinner.HexSpinner import HexSpinner


class BlockEditor(QWidget):
    """An editor for a block"""

    def __init__(self, parent: Optional[QWidget], block: AbstractBlock) -> None:
        super().__init__(parent)

        self.block = ObservableBlock.from_block(block)

        # Set up the layout of the block editor
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)

        # Allows editing the block through spinners
        def update_block_tiles(spinner_idx: int):
            """Updates the block's tiles by its respective spinner"""
            def update_block_tiles(i: int):
                tiles = self.block.tiles
                tiles[spinner_idx] = i
                self.block.tiles = tiles
            return update_block_tiles

        spinner_sides = ["top left", "bottom left", "top right", "bottom right"]
        for idx in range(4):
            spinner = HexSpinner(self, maximum=0xFF)
            spinner.setValue(self.block.tiles[idx])
            spinner.value_update_observable.attach_observer(update_block_tiles(idx))
            spinner.setWhatsThis(
                "<b>Block Editor</b>"
                "<br/>"
                f"Edit this spinner to change the {spinner_sides[idx]} tile."
                "<br/>"
            )
            x, y = idx & 1, idx // 2 * 2
            grid.addWidget(spinner, x, y)

        # A more gui friendly way to edit the gui.
        grid.addWidget(BlockTileEditor(self, self.block), 0, 1, 0, 1, Qt.AlignCenter)
        self.setLayout(grid)

        # Steal the block update observables, putting the responsibility on the block itself
        self.update_observable = GenericObservable("update")
        self.block.update_observable.attach_observer(self.update_observable.notify_observers)
        self.size_update_observable = GenericObservable("size_update")
        self.block.size_update_observable.attach_observer(self.size_update_observable.notify_observers)
        self.index_update_observable = GenericObservable("index_update")
        self.block.index_update_observable.attach_observer(self.index_update_observable.notify_observers)
        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.block.pattern_table_update_observable.attach_observer(self.pattern_table_update_observable.notify_observers)
        self.palette_set_update_observable = GenericObservable("palette_set_update")
        self.block.palette_set_update_observable.attach_observer(self.palette_set_update_observable.notify_observers)
        self.tsa_data_update_observable = GenericObservable("tsa_data_update")
        self.block.tsa_data_update_observable.attach_observer(self.tsa_data_update_observable.notify_observers)
        self.transparency_update_observable = GenericObservable("transparency_update")
        self.block.transparency_update_observable.attach_observer(self.transparency_update_observable.notify_observers)

        self.setWhatsThis(
            "<b>Block Editor</b>"
            "<br/>"
            "An editor for changing the 8x8 pixel tiles that composes a 16x16 block"
            "<br/>"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    @property
    def index(self) -> int:
        """The index the block is in for the tsa"""
        return self.block.index

    @index.setter
    def index(self, index: int) -> None:
        self.block.index = index

    @property
    def tsa_data(self) -> bytearray:
        """"The pattern table of the block"""
        return self.block.tsa_data

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        self.block.tsa_data = tsa_data

    @property
    def size(self) -> Size:
        """The size of the block in units of 16 pixels"""
        return self.block.size

    @size.setter
    def size(self, size: Size) -> None:
        self.block.size = size

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self.block.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self.block.pattern_table = pattern_table

    @property
    def palette_set(self) -> PaletteSet:
        """The palette currently used by the tsa"""
        return self.block.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self.block.palette_set = palette_set

    @property
    def transparency(self) -> bool:
        """Determines if the blocks will be transparent"""
        return self.block.transparency

    @transparency.setter
    def transparency(self, transparency: bool) -> None:
        self.block.transparency = transparency
