

from typing import Optional, List
from collections import namedtuple
from PySide2.QtWidgets import QComboBox, QWidget

from foundry.core.Observables.GenericObservable import GenericObservable


ComboBoxOption = namedtuple("ComboBoxOption", "callable")


class ComboBox(QComboBox):
    """A default combobox with extended observer functionality"""
    def __init__(self, parent: Optional[QWidget], options: Optional[List[ComboBoxOption]] = None) -> None:
        super().__init__(parent)

        # Push the index update slot to our API
        self.update_observable = GenericObservable("update")
        self.currentIndexChanged.connect(self.update_observable)

        self.items_count = 0
        if options is not None:
            for option in options:
                self.add_item(option)

    def add_item(self, option: ComboBoxOption) -> None:
        """Adds an item to the drop down with an action"""
        self.addItem(option.callable)
        index = self.items_count
        self.index_changed_action.observer.attach_observer(
            lambda result: option.callable() if result == index else result
        )
        self.items_count += 1

