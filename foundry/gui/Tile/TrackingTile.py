

from typing import Optional

from PySide2.QtWidgets import QWidget

from foundry.gui.Tile.WidgetTile import WidgetTile
from foundry.gui.QWidget.TrackingWidget import TrackingWidget
from foundry.gui.Tile.AbstractTile import AbstractTile


class TrackingTile(TrackingWidget, WidgetTile):
    """
    A Tile that tracks the movement and button presses of the mouse
    """

    def __init__(self, parent: Optional[QWidget], tile: AbstractTile) -> None:
        super().__init__(parent, tile)
