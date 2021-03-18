

from typing import Optional
from PySide2.QtWidgets import QWidget, QFormLayout, QSizePolicy

from foundry.gui.QLabel.Label import Label


class Panel(QWidget):
    """A panel that inherits the widgets actions"""
    def __init__(self, parent: Optional[QWidget], name: str, widget: QWidget):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QFormLayout()
        layout.setContentsMargins(1, 0, 1, 0)
        layout.addRow(Label.as_regular(self, name), widget)
        self.setLayout(layout)
