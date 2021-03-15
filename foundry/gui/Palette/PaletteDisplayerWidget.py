

from typing import Optional

from PySide2.QtWidgets import QWidget, QHBoxLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Palette.ObservablePalette import ObservablePalette
from foundry.core.Palette.Palette import Palette

from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget as ColorWidget


class PaletteDisplayerWidget(QWidget):
    """A widget to display a single palette"""
    def __init__(self, parent: Optional[QWidget], palette: Palette) -> None:
        super().__init__(parent)
        self._palette = ObservablePalette.from_palette(palette)

        self.update_observable = GenericObservable("update")
        self._palette.update_action.attach_observer(lambda pal: pal)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        for idx in range(3):
            button = ColorWidget.as_tiny(self, self.palette[idx + 1])
            # Connect the button to update automatically whenever the palette updates
            self.update_observable.attach_observer(lambda pal, i=idx, b=button: setattr(b, "color", pal[i]))
            hbox.addWidget(button)
        self.setLayout(hbox)

        self.setWhatsThis(
            "<b>Palette Editor</b>"
            "<br/>"
            "Edits a group of 3 colors"
            "<br/>"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.palette})"

    @property
    def palette(self) -> Palette:
        """The palette we are controlling"""
        return self._palette.palette

    @palette.setter
    def palette(self, palette: Palette) -> None:
        # Do not send an update unless we need to
        if palette != self.palette:
            self._palette.palette = palette
