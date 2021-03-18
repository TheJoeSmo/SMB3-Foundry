

from typing import Optional
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy


class Label(QLabel):
    """A generic spinner with extended functionality"""

    @classmethod
    def as_regular(cls, parent: Optional[QWidget], text: str):
        label = QLabel(parent)
        label.setText(text)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        label.setContentsMargins(0, 0, 0, 0)
        return label
