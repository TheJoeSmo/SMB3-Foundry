from copy import copy

from PySide2.QtWidgets import QWidget, QMessageBox

from core.TileSquareAssembly.ROM import ROM


class ROMResolver:
    def __init__(self, parent: QWidget):
        self.parent = parent

    def __call__(self, primary: ROM, secondary: ROM):
        answer = QMessageBox.question(
            self.parent,
            "Please confirm",
            """
There seems to be changes from an external source.
Would you like to keep these changes?
Warning: This will overwrite the current information.""",
            QMessageBox.No | QMessageBox.Yes,
            QMessageBox.No,
        )

        if answer:
            return copy(secondary)
        else:
            return copy(primary)
