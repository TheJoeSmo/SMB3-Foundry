

from typing import Optional
from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtGui import Qt

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Size.Size import Size

from foundry.gui.Block.BlockTileEditor import BlockTileEditor
from foundry.gui.Block.ObservableBlock import ObservableBlock
from foundry.core.Block.AbstractBlock import AbstractBlock
from foundry.gui.QSpinner.HexSpinner import HexSpinner


class BlockEditor(QWidget):
    """An editor for a block"""

    def __init__(self, parent: Optional[QWidget], block: AbstractBlock) -> None:
        super().__init__(parent)

        self._block = ObservableBlock.from_block(block)

        # Steal the block update observables, putting the responsibility on the block itself
        self.update_observable = GenericObservable("update")
        self.update_observable.attach_observer(lambda *_: self.update)
        self.block.update_observable.attach_observer(self.update_observable.notify_observers)
        self.size_update_observable = GenericObservable("size_update")
        self.block.size_update_observable.attach_observer(self.size_update_observable.notify_observers)
        self.index_update_observable = GenericObservable("index_update")
        self.block.index_update_observable.attach_observer(self.index_update_observable.notify_observers)
        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.block.pattern_table_update_observable.attach_observer(
            self.pattern_table_update_observable.notify_observers)
        self.palette_set_update_observable = GenericObservable("palette_set_update")
        self.block.palette_set_update_observable.attach_observer(self.palette_set_update_observable.notify_observers)
        self.tsa_data_update_observable = GenericObservable("tsa_data_update")
        self.block.tsa_data_update_observable.attach_observer(self.tsa_data_update_observable.notify_observers)
        self.transparency_update_observable = GenericObservable("transparency_update")
        self.block.transparency_update_observable.attach_observer(self.transparency_update_observable.notify_observers)

        # Set up the layout of the block editor
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)

        # Allows editing the block through spinners
        def update_block_tiles(spinner_idx: int):
            """Updates the block's tiles by its respective spinner"""
            def update_block_tiles(i: int):
                tiles = list(self.block.tiles)
                if tiles[spinner_idx] != i:
                    tiles[spinner_idx] = i
                    self._block.tiles = tuple(tiles)
            return update_block_tiles

        def update_spinners(spinner_idx: int):
            """Refresh the spinners when needed"""
            def update_spinner(*args, **kwargs):
                spinners[spinner_idx].value_update_observable.silenced = True
                spinners[spinner_idx].text_update_observable.silenced = True
                spinners[spinner_idx].setValue(self.block.tiles[spinner_idx])
                spinners[spinner_idx].value_update_observable.silenced = False
                spinners[spinner_idx].text_update_observable.silenced = False
            return update_spinner

        spinner_sides = ["top left", "bottom left", "top right", "bottom right"]
        spinners = []
        for idx in range(4):
            spinners.append(HexSpinner(self, maximum=0xFF))
            spinners[idx].setValue(self.block.tiles[idx])
            spinners[idx].value_update_observable.attach_observer(update_block_tiles(idx))
            self.index_update_observable.attach_observer(update_spinners(idx))
            self.tsa_data_update_observable.attach_observer(update_spinners(idx))
            spinners[idx].setWhatsThis(
                "<b>Block Editor</b>"
                "<br/>"
                f"Edit this spinner to change the {spinner_sides[idx]} tile."
                "<br/>"
            )
            x, y = idx & 1, idx // 2 * 2
            grid.addWidget(spinners[idx], x, y)

        # A more gui friendly way to edit the gui.
        block_editor = BlockTileEditor(self, self.block)

        # Send the block editor updates, as it just has a copy of the actual block
        def update_block_editor_size(size: Size):
            block_editor._block.size = size
        self._block.size_update_observable.attach_observer(update_block_editor_size)

        def update_block_editor_index(index: int):
            block_editor._block.index = index
        self.index_update_observable.attach_observer(update_block_editor_index)

        def update_block_editor_tsa_data(tsa_data: bytearray):
            block_editor._block.tsa_data = tsa_data
        self.tsa_data_update_observable.attach_observer(update_block_editor_tsa_data)

        def update_block_editor_pattern_table(pattern_table: PatternTable):
            block_editor._block.pattern_table.pattern_table = pattern_table
        self.pattern_table_update_observable.attach_observer(update_block_editor_pattern_table)

        def update_block_editor_palette_set(palette_set: PaletteSet):
            block_editor._block.palette = palette_set[self._block.index // 0x40]
        self.palette_set_update_observable.attach_observer(update_block_editor_palette_set)

        grid.addWidget(block_editor, 0, 1, 0, 1, Qt.AlignCenter)
        self.setLayout(grid)

        self.setWhatsThis(
            "<b>Block Editor</b>"
            "<br/>"
            "An editor for changing the 8x8 pixel tiles that composes a 16x16 block"
            "<br/>"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.block})"

    @property
    def block(self) -> ObservableBlock:
        return self._block  # Don't set the block or bad things happen

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
