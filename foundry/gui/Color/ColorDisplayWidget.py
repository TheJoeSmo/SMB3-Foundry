

from typing import Optional
from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QColor
from PySide2.QtCore import QSize

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Color.Color import Color
from foundry.core.Color.ObservableColor import ObservableColor


class ColorDisplayWidget(QWidget):
    """A generic tool button with extended functionality"""
    def __init__(self, parent: Optional[QWidget], color: Color):
        super().__init__(parent)
        # Pass the job of handling the color to the observable color
        self.setAutoFillBackground(True)

        self._color = ObservableColor(0, 0, 0)

        self.update_observable = GenericObservable("update")

        # Update the background and send updates upstream
        def update_bg(c: Color):
            pal = self.palette()
            pal.setColor(self.backgroundRole(), QColor(c.red, c.green, c.blue))
            self.setPalette(pal)

        self._color.update_action.attach_observer(
            lambda c: update_bg(c)
        )
        self.color = color  # Push the new colors
        self._color.update_action.attach_observer(
            lambda c: self.update_observable.notify_observers(c)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.color})"

    def sizeHint(self) -> QSize:
        """The size hint for the button"""
        return QSize(20, 20)

    @property
    def color(self) -> Color:
        """Returns the current color of the button"""
        return self._color.color

    @color.setter
    def color(self, color: Color) -> None:
        self._color.color = color

    @classmethod
    def as_tiny(cls, *args, **kwargs):
        """Makes a tiny push button"""
        button = cls(*args, **kwargs)
        button.setBaseSize(20, 20)
        button.setMinimumWidth(20)
        button.setMinimumHeight(20)
        return button
