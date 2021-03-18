

from PySide2.QtWidgets import QSizePolicy, QToolBar, QWidget
from PySide2.QtGui import Qt


class Toolbar(QToolBar):
    """An extension of the QToolBar with extended functionality"""
    @classmethod
    def default_toolbox(cls, parent: QWidget, name: str, widget: QWidget, side: int) -> "Toolbar":
        """Makes a default toolbox"""
        # Creates the toolbar
        toolbar = QToolBar(name, parent)

        # Sets the policies to allow it to be moved
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        toolbar.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        toolbar.setOrientation(Qt.Horizontal)
        toolbar.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea | Qt.TopToolBarArea | Qt.BottomToolBarArea)
        toolbar.setFloatable(True)

        # Add the main widget to the toolbar
        toolbar.addWidget(widget)

        # Add it to the parent automatically
        parent.addToolBar(side, toolbar)
        return toolbar