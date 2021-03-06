"""
This module contains the base functionality for spinners
Spinner: A generic spinner with extended functionality
SpinnerPanel: A generic spinner with a label
"""

from typing import Optional, List
from PySide2.QtWidgets import QSpinBox, QWidget

from foundry.gui.QCore.util import DefaultSizePartial
from foundry.core.Action.Action import Action
from foundry.core.Action.AbstractActionObject import AbstractActionObject


class Spinner(QSpinBox, AbstractActionObject, DefaultSizePartial):
    """A generic spinner with extended functionality"""
    value_changed_action: Action  # Updates when the value inside the spinner changes
    text_changed_action: Action  # Updates when the text inside the spinner changes

    def __init__(self, parent: Optional[QWidget], minimum=0, maximum=0xFFFFFF):
        QSpinBox.__init__(self, parent)
        AbstractActionObject.__init__(self)
        DefaultSizePartial.__init__(self)
        self.parent = parent

        self.setRange(minimum, maximum)

    def get_actions(self) -> List[Action]:
        """Gets the actions for the object"""
        return [
            Action.from_signal(
                "value_changed", self.valueChanged, observer_name=f"{self.__class__.__name__} Value Updated"
            ),
            Action.from_signal(
                "text_changed", self.textChanged, observer_name=f"{self.__class__.__name__} Text Updated"
            ),
        ]
