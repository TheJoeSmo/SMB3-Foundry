

from typing import Optional

from PySide2.QtWidgets import QWidget, QHBoxLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Palette.ObservablePalette import ObservablePalette
from foundry.core.Palette.Palette import Palette

from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget as ColorWidget


class PaletteDisplayerWidget(QWidget):
    """A widget to display a single palette"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Palette Displayer</b><br>Displays the colors of the palette<br/>"

    def __init__(self, parent: Optional[QWidget], palette: Palette, full=False) -> None:
        super().__init__(parent)
        self._palette = ObservablePalette.from_palette(palette)

        self.update_observable = GenericObservable("update")
        self._palette.update_action.attach_observer(lambda pal: pal)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        for idx in range(4 if full else 3):
            button = self._load_button(idx, full)
            # Connect the button to update automatically whenever the palette updates
            self.update_observable.attach_observer(lambda pal, i=idx, b=button: setattr(b, "color", pal[i]))
            hbox.addWidget(button)
        self.setLayout(hbox)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.palette})"

    def _load_button(self, idx: int, full: bool) -> QWidget:
        return ColorWidget.as_tiny(self, self.palette[idx if full else idx + 1])

    @property
    def palette(self) -> Palette:
        """The palette we are controlling"""
        return self._palette.palette

    @palette.setter
    def palette(self, palette: Palette) -> None:
        # Do not send an update unless we need to
        if palette != self.palette:
            self._palette.palette = palette
