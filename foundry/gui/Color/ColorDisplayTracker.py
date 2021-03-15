

from typing import Optional
from PySide2.QtWidgets import QWidget

from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget
from foundry.gui.QWidget.TrackingWidget import TrackingWidget

from foundry.core.Color.Color import Color


class ColorDisplayTracker(TrackingWidget, ColorDisplayWidget):
    """A colored button that records when it is pressed"""
    def __init__(self, parent: Optional[QWidget], color: Color):
        super().__init__(parent, color)
