

from typing import Optional

from PySide2.QtWidgets import QWidget, QHBoxLayout

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.PaletteSet.ObservablePaletteSet import ObservablePaletteSet
from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.gui.Color.ColorDisplayWidget import ColorDisplayWidget as ColorWidget
from foundry.gui.Palette.PaletteDisplayerWidget import PaletteDisplayerWidget as PaletteWidget


class PaletteSetDisplayerWidget(QWidget):
    """A widget to display a set of palettes"""

    # The text that will be displayed as a tool tip
    whats_this_text = "<b>Palette Set Displayer</b><br>Displays an entire palette set<br/>"

    def __init__(self, parent: Optional[QWidget], palette_set: PaletteSet, show_background_color=False) -> None:
        super().__init__(parent)
        self._palette_set = ObservablePaletteSet.from_palette(palette_set)

        self.update_observable = GenericObservable("update")
        self._palette_set.update_action.attach_observer(lambda pal: pal)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        if show_background_color:
            button = self._load_button()
            # Connect the button to update automatically whenever the palette set updates
            self.update_observable.attach_observer(lambda pal, b=button: setattr(b, "color", pal[0][0]))
            hbox.addWidget(button)
        for idx in range(4):
            button = self._load_palette(idx)
            # Connect the button to update automatically whenever the palette set updates
            self.update_observable.attach_observer(lambda pal, i=idx, b=button: setattr(b, "palette", pal[i]))
            hbox.addWidget(button)
        self.setLayout(hbox)

        self.setWhatsThis(self.whats_this_text)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parent}, {self.palette_set})"

    def _load_button(self) -> QWidget:
        return ColorWidget.as_tiny(self, self.palette_set[0][0])

    def _load_palette(self, idx: int) -> QWidget:
        return PaletteWidget(self, self.palette_set[idx])

    @property
    def palette_set(self) -> PaletteSet:
        """The palette we are controlling"""
        return self._palette_set.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        # Do not send an update unless we need to
        if palette_set != self.palette_set:
            self._palette_set.palette_set = palette_set
