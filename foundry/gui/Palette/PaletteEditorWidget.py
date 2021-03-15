

from typing import Optional

from PySide2.QtWidgets import QWidget

from foundry.core.Palette.Palette import Palette

from foundry.gui.QWidget.TrackingWidget import TrackingWidget
from foundry.gui.Palette.PaletteDisplayerWidget import PaletteDisplayerWidget
from foundry.gui.Color.ColorWidget import ColorPickerButton as ColorWidget


class PaletteEditorWidget(TrackingWidget, PaletteDisplayerWidget):
    """A widget to display a single palette"""

    whats_this_text = "<b>Palette Editor</b><br>A widget to edit a palette<br/>"

    def __init__(self, parent: Optional[QWidget], palette: Palette, full: bool) -> None:
        super().__init__(parent, palette, full)

    def _load_button(self, idx: int, full: bool) -> QWidget:
        def set_color(color):
            # Update the palette to incorporate the new color
            palette = self.palette
            palette[idx] = color
            self.palette = palette

        button = ColorWidget.as_tiny(self, self.palette[idx if full else idx + 1])
        button.update_action.attach_observer(lambda color, *_: set_color(color))
        return button
