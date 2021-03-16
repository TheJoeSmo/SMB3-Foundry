

from typing import Optional, Callable
from PySide2.QtWidgets import QVBoxLayout

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler
from foundry.core.Palette.Palette import Palette
from foundry.core.Size.Size import Size

from foundry.gui.Tile.PatternTableTilePicker import PatternTableTilePicker as TilePicker
from foundry.gui.Dialog.Dialog import Dialog


class ColorPickerPopup(Dialog):
    """Allows you to pick a custom color and returns the value"""

    def __init__(
            self,
            parent,
            palette: Palette,
            pattern_table: PatternTableHandler,
            size: Optional[Size] = None,
            title="Select a Tile",
            action: Optional[Callable] = None
    ) -> None:
        super().__init__(parent, title)

        layout = QVBoxLayout(self)
        self.tile_picker = TilePicker(self, palette, pattern_table, size)
        layout.addWidget(self.color_picker)
        self.setLayout(layout)

        self.tile_picker.update_action.attach_observer(lambda *_: self.accept())
        if action is not None:
            self.color_picker.update_action.attach_observer(action)

        self.setWhatsThis(self.tile_picker.whats_this_text)  # Steal the what this is text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, " \
               f"{self.tile_picker.tile_palette}, {self.tile_picker.pattern_table}," \
               f"{self.tile_picker.size}, {self.title}, {self.action})"
