

from typing import Optional
from PySide2.QtWidgets import QSpinBox, QWidget

from foundry.core.Observables.GenericObservable import GenericObservable


class Spinner(QSpinBox):
    """A generic spinner with extended functionality"""

    def __init__(self, parent: Optional[QWidget], minimum=0, maximum=0xFFFFFF):
        super().__init__(parent)

        self.value_update_observable = GenericObservable("value_update")
        self.valueChanged.connect(lambda *args, **kwargs: self.value_update_observable.notify_observers(*args, **kwargs))
        self.text_update_observable = GenericObservable("text_update")
        self.textChanged.connect(lambda *args, **kwargs: self.text_update_observable.notify_observers(*args, **kwargs))

        self.setRange(minimum, maximum)
