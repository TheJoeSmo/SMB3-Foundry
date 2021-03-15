

from typing import Optional

from PySide2.QtWidgets import QWidget

from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.gui.PaletteSet.PaletteSetDisplayerWidget import PaletteSetDisplayerWidget
from foundry.gui.Color.ColorWidget import ColorPickerButton as ColorWidget
from foundry.gui.Palette.PaletteEditorWidget import PaletteEditorWidget as PaletteWidget


class PaletteSetEditorWidget(PaletteSetDisplayerWidget):
    """A widget to display a single palette"""

    whats_this_text = "<b>Palette Set Editor</b><br>Allows the editing of an entire palette set<br/>"

    def __init__(self, parent: Optional[QWidget], palette_set: PaletteSet, show_background_color=False) -> None:
        super().__init__(parent, palette_set, show_background_color)

    def _load_button(self) -> QWidget:
        def set_background_color(color):
            palette_set = self.palette_set
            palette_set[0][0] = color
            self.palette_set = palette_set

        button = ColorWidget.as_tiny(self, self.palette_set[0][0])
        button.update_observable.attach_observer(lambda color, *_: set_background_color(color))
        return button

    def _load_palette(self, idx: int) -> QWidget:
        def set_palette(palette):
            # Update the palette set to incorporate the new palette
            palette_set = self.palette_set
            palette_set[idx] = palette
            self.palette_set = palette_set

        button = PaletteWidget(self, self.palette_set[idx], False)
        button.update_observable.attach_observer(lambda palette, *_: set_palette(palette))
        return button
