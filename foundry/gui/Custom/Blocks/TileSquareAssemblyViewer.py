

from typing import Optional, List

from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtGui import Qt

from foundry.core.geometry.Size.Size import Size
from foundry.core.Settings.util import get_setting
from foundry.core.Observables.ObservableDecorator import ObservableDecorator
from foundry.core.Action.Action import Action

from foundry.game.gfx.PatternTableHandler import PatternTableHandler
from foundry.game.gfx.Palette import PaletteSet
from foundry.gui.Custom.Block.Block import Block

from foundry.gui.QCore.Tracker import AbstractActionObject
from foundry.gui.Custom.Block.BlockTrackingObject import BlockTrackingObject
from foundry.gui.QCore import MARGIN_TIGHT
from foundry.gui.QWidget import Widget


class TileSquareAssemblyViewer(Widget, AbstractActionObject):
    """A widget that views the TSA"""
    refresh_event_action: Action  # Used internally for redrawing the widget
    size_update_action: Action  # Updates when the size updates
    tsa_data_update_action: Action  # Updates when the tsa offset updates
    palette_set_update_action: Action  # Updates when the palette set updates
    pattern_table_update_action: Action  # Update when the pattern table updates

    """Views the tile in a given tsa"""
    def __init__(
            self,
            parent: Optional[QWidget],
            ptn_tbl: PatternTableHandler,
            pal_set: PaletteSet,
            tsa_data: bytearray
            ) -> None:
        Widget.__init__(self, parent)
        AbstractActionObject.__init__(self)
        self.parent = parent
        self.blocks = []
        self.pattern_table = ptn_tbl
        self.palette_set = pal_set
        self.size = Size(1, 1)
        self.tsa_data = tsa_data

        self._set_up_layout()

    @classmethod
    def from_tsa(
            cls,
            parent: Optional[QWidget],
            ptn_tbl: PatternTableHandler,
            pal_set: PaletteSet,
            tsa_offset: int
    ):
        """Generates a TSA viewer from a given offset"""
        return cls(parent, ptn_tbl, pal_set, cls.tsa_data_from_tsa_offset(tsa_offset))

    def _set_up_layout(self) -> None:
        """Returns the widgets layout"""
        grid_layout = QGridLayout()
        grid_layout.setSpacing(MARGIN_TIGHT)
        grid_layout.setDefaultPositioning(0x10, Qt.Horizontal)
        for idx in range(0x100):
            sprite = BlockTrackingObject(
                self, f"block_{idx}", Block(
                    self.size, idx, self.pattern_table, self.palette_set, self.tsa_data, self.transparency)
            )
            self.blocks.append(sprite)
            grid_layout.addWidget(sprite)

        self.setLayout(grid_layout)

    def get_actions(self) -> List[Action]:
        """Gets the actions for the object"""
        return [
            Action("refresh_event", ObservableDecorator(lambda *_: self.update())),
            Action("size_update", ObservableDecorator(lambda size: size)),
            Action("tsa_data_update", ObservableDecorator(lambda tsa_offset: tsa_offset)),
            Action("palette_set_update", ObservableDecorator(lambda palette_set: palette_set)),
            Action("pattern_table_update", ObservableDecorator(lambda pattern_table: pattern_table)),
        ]

    @staticmethod
    def tsa_data_from_tsa_offset(tsa_offset: int) -> bytearray:
        """Returns the tsa data from a given offset"""
        from foundry.game.File import ROM, TSA_TABLE_SIZE, TSA_TABLE_INTERVAL
        return ROM().bulk_read(TSA_TABLE_SIZE, (tsa_offset * TSA_TABLE_INTERVAL) + 0x10)

    @property
    def tsa_data(self) -> bytearray:
        """Find the tsa data from a given offset"""
        return self._tsa_data

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        self._tsa_data = tsa_data
        for block in self.blocks:
            block.tsa_data = self._tsa_data
        self.tsa_data_update_action(self.tsa_data)
        self.refresh_event_action()

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table for the tiles"""
        return self._pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTableHandler) -> None:
        self._pattern_table = pattern_table
        for block in self.blocks:
            block.pattern_table = pattern_table
        self.pattern_table_update_action(self._pattern_table)
        self.refresh_event_action()

    @property
    def size(self) -> Size:
        """The size of the blocks"""
        return self._size

    @size.setter
    def size(self, size: Size) -> None:
        self._size = size
        for block in self.blocks:
            block.size = size
        self.size_update_action(self._size)
        self.refresh_event_action()

    @property
    def palette_set(self) -> PaletteSet:
        """The palette currently used by the tsa"""
        return self._palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self._palette_set = palette_set
        for block in self.blocks:
            block.palette_set = palette_set
        self.palette_set_update_action(self._palette_set)
        self.refresh_event_action()

    @property
    def transparency(self) -> bool:
        """Determines if the blocks will be transparent"""
        return get_setting("block_transparency", True)

