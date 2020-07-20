"""
The container for all the local file menu functions
"""

from typing import Callable
from PySide2.QtWidgets import QMenu, QAction, QMessageBox, QFileDialog
from abc import abstractmethod, ABC

from foundry.decorators.Required import Required, SmartRequired
from foundry.decorators.Observer import Observed, ObservedAndRequired


class Menu(QMenu):
    """A default menu"""
    def __init__(self, parent, title="", *args, **kwargs) -> None:
        super().__init__(parent=parent, title=title)
        self.parent = parent

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent})"

    """The custom extensions for the QMenu class"""
    def add_action(self, name: str, on_click: Callable) -> QAction:
        """
        Adds an item to the list automatically and makes a trigger that connects to the callable
        :param name: The name of the menu item
        :param on_click: The callable to be called
        :return: None
        """
        action = self.addAction(name)
        action.triggered.connect(on_click)
        return action


class MenuElement:
    """An element of a menu"""
    def __init__(self, parent: Menu, add_action: bool = True) -> None:
        self.parent = parent
        if add_action:
            self.parent.add_action(self.name, self.action)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.parent})"

    @property
    @abstractmethod
    def base_name(self) -> str:
        """The base name of the element"""

    @property
    def bold(self) -> bool:
        """Determines if the element is bold"""
        return False

    @property
    def italic(self) -> bool:
        """Determines if the element is italic"""
        return False

    @property
    def name(self) -> str:
        """The real name of the element"""
        return f"{'*' if self.italic else ''}{'&' if self.bold else ''}{self.base_name}"

    @abstractmethod
    def action(self) -> None:
        """The action to be called"""


class MenuElementSafe(MenuElement, ABC):
    """A Menu Element that contains a test to see if something is safe to do"""
    def __init__(self, parent, add_action: bool = True) -> None:
        self.find_warnings = SmartRequired(self.find_warnings)
        super().__init__(parent, add_action)
        self.path_to_rom = ""
        self.action.attach_required(observer=self.safe_to_change)

    @property
    def path(self) -> str:
        """Gets the path to the desired location"""
        return QFileDialog.getOpenFileName(self.parent, caption=self.caption, filter=self.file_filter)[0]

    @property
    @abstractmethod
    def caption(self) -> str:
        """Provides the caption to ask for a file"""

    @property
    @abstractmethod
    def file_filter(self) -> str:
        """Provides the filter for finding the desired file"""

    def find_warnings(self):
        """Returns true or false depending if we make it through all the routines"""
        return True, '', ''

    def safe_to_change(self) -> bool:
        """Determines if it is safe to change"""
        safe, reason, additional_info = self.find_warnings()

        if safe:
            return True
        else:
            answer = QMessageBox.warning(
                self.parent,
                reason,
                f"{additional_info}\n\nDo you want to proceed?",
                QMessageBox.No | QMessageBox.Yes,
                QMessageBox.No,
            )
            return answer == QMessageBox.Yes

    @abstractmethod
    def action(self) -> bool:
        """The action of the object"""


class MenuElementOpen(MenuElementSafe, ABC):
    """A Menu Element that contains tests required for opening"""
    def __init__(self, parent, add_action: bool = True) -> None:
        self.action = ObservedAndRequired(self.action)
        self.open = Observed(self.open)
        super().__init__(parent, add_action)

    def action(self):
        """Routine for handling the entire opening process"""
        path = self.path
        if not path:
            return False

        try:
            self.open(path)
        except IOError as exp:
            QMessageBox.warning(self.parent, type(exp).__name__, f"Cannot open file '{path}'.")
            return False
        return True

    def open(self, path: str) -> str:
        """Opens a file from a path"""
        return path


class MenuElementSave(MenuElementSafe, ABC):
    """A Menu Element that contains tests required for saving"""
    def __init__(self, parent, add_action: bool = True) -> None:
        self.save = Observed(self.save)
        self.can_change = Required(self.can_change)
        self.action = ObservedAndRequired(self.action)
        super().__init__(parent, add_action)
        self.action.attach_required(observer=self.can_change)

    @property
    def path(self) -> str:
        """Gets the path to the desired location"""
        return QFileDialog.getSaveFileName(self.parent, caption=self.caption, filter=self.file_filter)[0]

    def can_change(self) -> bool:
        """Determines if it is safe to change"""
        return True

    def action(self):
        """Routine for handling the entire saving process"""
        path = self.path
        if not path:
            return False

        try:
            self.save(path)
        except IOError as exp:
            QMessageBox.warning(
                self.parent, f"{type(exp).__name__}", f"Cannot save ROM data to file '{path}'."
            )
            return False
        return True

    def save(self, path: str = "") -> str:
        """Saves to the file from path"""
        return path