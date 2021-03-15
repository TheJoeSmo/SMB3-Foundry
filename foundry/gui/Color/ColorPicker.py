

from typing import Optional

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QGridLayout

from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget as ColorButton


from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Color.PaletteController import PaletteController

_palette_controller = PaletteController()


class ColorPicker(QWidget):
    """A widget to help with picking a NES color"""
    def __init__(self, parent: Optional[QWidget]) -> None:
        super().__init__(parent)

        self.update_action = GenericObservable("update")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)
        grid_layout.setDefaultPositioning(0x10, Qt.Horizontal)

        # Generate the 40 different NES colors and attach a observer that sends the update upstream to them
        for idx in range(0x40):
            button = ColorButton.as_tiny(self, _palette_controller.colors[idx])
            button.update_observable.attach_observer(lambda color, i=idx: self.update_action((i, color)))
            grid_layout.addWidget(button, row=idx % 0x10, column=idx // 0x10)

        self.setLayout(grid_layout)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent})"