

from typing import Optional, Union
from PySide2.QtWidgets import QWidget

from foundry.gui.Color.ColorPickerPopUp import ColorPickerPopup
from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget
from foundry.gui.QWidget.TrackingWidget import TrackingWidget

from foundry.core.Color.Color import Color
from foundry.core.Color.PaletteController import PaletteController

_palette_controller = PaletteController()


class ColorPickerButton(TrackingWidget, ColorDisplayWidget):
    """A colored button that pops up a dialog whenever clicked"""
    def __init__(self, parent: Optional[QWidget], color: Union[int, Color]):
        # Accept an NES color index or an actual color
        if isinstance(color, int):
            color = _palette_controller.colors[color]

        super().__init__(parent, color)
        self.index_needs_updated = True  # Signals when the index has not been updated

        # Whenever the widget is double clicked the widget will bring up a popup to select a color
        self.double_click_observable.attach_observer(
            lambda *_: ColorPickerPopup(self, action=lambda _, c: setattr(self, "color", c)).exec_()
        )

        self.setWhatsThis(
            "<b>Color Picker</b><br/>"
            "Double click me to change my color<br/>"
        )

    @property
    def color_index(self) -> int:
        """Returns the current color index of the button"""
        return _palette_controller.colors_inverse[self._color.color]  # Private color is used to be a bit faster
