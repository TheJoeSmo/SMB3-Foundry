

from typing import Optional, Tuple

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Observables.SilencerGenericObservable import SilencerGenericObservable
from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PaletteSet.ObservablePaletteSet import ObservablePaletteSet
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Size.ObservableSize import ObservableSize
from foundry.core.Size.Size import Size

from foundry.gui.Block.Block import Block

from foundry.gui.Block.AbstractBlock import AbstractBlock


class ObservableBlock(AbstractBlock):
    """Provides automatic updates """

    def __init__(
            self,
            size: Optional[Size],
            index: int,
            ptn_tbl: PatternTableHandler,
            pal_set: PaletteSet,
            tsa_data: bytearray,
            transparency: bool = True
    ) -> None:

        self._observed_block = Block(
            observable_size := ObservableSize.from_size(size),
            index,
            ptn_tbl,
            observable_pal := ObservablePaletteSet.from_palette_set(pal_set),
            tsa_data,
            transparency
        )

        # Set up observables and connect them so update will be a catch all observable
        # Has the ability to be silenced for specific operations where multiple updates are not ideal
        self.update_observable = SilencerGenericObservable("update")

        self.size_update_observable = GenericObservable("size_update")
        self.size_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        observable_size.size_update_observable.attach_observer(self.size_update_observable.notify_observers)

        self.index_update_observable = GenericObservable("index_update")
        self.index_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.pattern_table_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        # Checks for updates are handled by the internal pattern table of the handler
        self.pattern_table.pattern_table.page_update_observable.attach_observer(
            self.pattern_table_update_observable.notify_observers
        )

        self.palette_set_update_observable = GenericObservable("palette_set_update")
        self.palette_set_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        observable_pal.palette_set_update_observable.attach_observer(self.palette_set_update_observable.notify_observers)

        self.tsa_data_update_observable = GenericObservable("tsa_data_update")
        self.tsa_data_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

        self.transparency_update_observable = GenericObservable("transparency_update")
        self.transparency_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.size}, {self.index}, {self.pattern_table}, " \
               f"{self.palette_set}, {self.tsa_data}, {self.transparency})"

    @property
    def size(self) -> Size:
        """The size of the block in units of 16 pixels"""
        return self._observed_block.size

    @size.setter
    def size(self, size: Size) -> None:
        self._observed_block.size.size = size

    @property
    def index(self) -> int:
        """The index of the block"""
        return self._observed_block.index

    @index.setter
    def index(self, index: int) -> None:
        self._observed_block.index = index
        self.index_update_observable.notify_observers(index)

    @property
    def tsa_data(self) -> bytearray:
        """Find the tsa data from a given offset"""
        return self._observed_block.tsa_data

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        self._observed_block.tsa_data = tsa_data
        self.tsa_data_update_observable.notify_observers(tsa_data)

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self._observed_block.pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self._observed_block.pattern_table.pattern_table = pattern_table.pattern_table

    @property
    def palette_set(self) -> PaletteSet:
        """The palette currently used by the tsa"""
        return self._observed_block.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self.observed_block.palette_set.palette_set = palette_set

    @property
    def transparency(self) -> bool:
        """Determines if the blocks will be transparent"""
        return self._observed_block.transparency

    @transparency.setter
    def transparency(self, transparency: bool) -> None:
        self.observed_block.transparency = transparency
        self.transparency_update_observable.notify_observers(transparency)

    @property
    def tiles(self) -> Tuple[int]:
        return self._observed_block.tiles

    @tiles.setter
    def tiles(self, tiles: Tuple[int]):
        self.observed_block.tiles = tiles
        self.tsa_data_update_observable.notify_observers(self.tsa_data)

    @property
    def observed_block(self) -> Block:
        return Block(self.size, self.index, self.pattern_table, self.palette_set, self.tsa_data, self.transparency)

    @observed_block.setter
    def observed_block(self, block: Block) -> None:
        if self._observed_block != block:
            # Silence the update, to prevent unnecessary updates.
            self.update_observable.silenced = True
            self.size, self.index, self.pattern_table = block.size, block.index, block.pattern_table
            self.palette_set, self.tsa_data, self.transparency = block.palette_set, block.tsa_data, block.transparency
            # Send an update, as we decided to handle it manually
            self.update_observable.silenced = False
            self.update_observable.notify_observers()
