

from typing import Optional

from PySide2.QtWidgets import QWidget

from foundry.gui.Block.WidgetBlock import WidgetBlock
from foundry.gui.QWidget.TrackingWidget import TrackingWidget
from foundry.gui.Block.AbstractBlock import AbstractBlock


class TrackingBlock(TrackingWidget, WidgetBlock):
    """
    A block that tracks the movement and button presses of the mouse
    """

    def __init__(self, parent: Optional[QWidget], block: AbstractBlock) -> None:
        super().__init__(parent, block)
