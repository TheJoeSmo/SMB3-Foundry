

from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QMouseEvent
from PySide2.QtCore import QTimer, Qt

from foundry.core.Observables.GenericObservable import GenericObservable


SINGLE_CLICK = 0  # default value for a single click
DOUBLE_CLICK = 1  # default value for a double click


class TrackingWidget(QWidget):
    """
    Connects the QT to the observer system and automatically adds double clicking.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last = None
        self.setMouseTracking(True)

        self.pressed_observable = GenericObservable("pressed")
        self.released_observable = GenericObservable("released")
        self.single_click_observable = GenericObservable("single_click")
        self.double_click_observable = GenericObservable("double_click")
        self.mouse_moved_observable = GenericObservable("moused_moved")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handles a button being pressed"""
        self.pressed_observable.notify_observers(event.button())
        self.last = SINGLE_CLICK

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Handles a button being released"""
        self.released_observable.notify_observers(event.button())
        if self.last == SINGLE_CLICK:
            button = event.button()
            QTimer.singleShot(QApplication.instance().doubleClickInterval(), lambda *_: self.single_click_event(button))
        else:
            self.double_click_event(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handles the mouse moving"""
        self.mouse_moved_observable.notify_observers(event.pos())

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handles a button being double pressed"""
        self.last = DOUBLE_CLICK

    def double_click_event(self, event: QMouseEvent):
        """Handles a button being double clicked"""
        self.double_click_observable.notify_observers(event.button())

    def single_click_event(self, button: Qt.MouseButton):
        """Handles a button being single clicked"""
        self.single_click_observable.notify_observers(button)
