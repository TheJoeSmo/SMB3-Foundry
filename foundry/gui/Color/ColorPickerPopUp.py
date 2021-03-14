

from typing import Optional, Callable
from PySide2.QtWidgets import QVBoxLayout

from foundry.gui.Color.ColorPicker import ColorPicker
from foundry.gui.Dialog.Dialog import Dialog


class ColorPickerPopup(Dialog):
    """Allows you to pick a custom color and returns the value"""

    def __init__(self, parent, title="Select a Color", action: Optional[Callable] = None) -> None:
        super().__init__(parent, title)

        layout = QVBoxLayout(self)
        self.color_picker = ColorPicker(self)
        layout.addWidget(self.color_picker)
        self.setLayout(layout)

        self.color_picker.update_action.attach_observer(lambda *_: self.accept())
        if action is not None:
            self.color_picker.update_action.attach_observer(lambda idx, color: action(idx, color))

        self.setWhatsThis(
            "<b>Color Picker Popup</b>"
            "<br/>"
            "Click the desired color"
            "<br/>"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.title}, {self.action})"