

from typing import Optional
from PySide2.QtGui import Qt, QKeyEvent
from PySide2.QtWidgets import QDialog, QSizePolicy


class Dialog(QDialog):
    """This class makes the default Dialog window"""
    def __init__(self, parent, title: Optional[str] = None):
        super().__init__(self, parent)
        if title is not None:
            self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def keyPressEvent(self, event: QKeyEvent):
        """The action when a key is pressed"""
        if event.key() == Qt.Key_Escape:
            self.on_exit()

    def on_exit(self):
        """When the dialog is being exited"""
        self.hide()

    def closeEvent(self, event):
        """When the dialog is being closed"""
        self.on_exit()
