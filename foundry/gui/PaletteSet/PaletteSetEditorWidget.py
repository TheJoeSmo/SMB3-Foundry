

from typing import Optional

from PySide2.QtWidgets import QWidget

from foundry.core.PaletteSet.PaletteSet import PaletteSet

from foundry.gui.PaletteSet.PaletteSetDisplayerWidget import PaletteSetDisplayerWidget
from foundry.gui.Color.ColorWidget import ColorPickerButton as ColorWidget
from foundry.gui.Palette.PaletteEditorWidget import PaletteEditorWidget as PaletteWidget


class PaletteSetEditorWidget(PaletteSetDisplayerWidget):
    """A widget to display a single palette"""

    whats_this_text = "<b>Palette Set Editor</b><br>Allows the editing of an entire palette set<br/>"

    def __init__(self, parent: Optional[QWidget], palette_set: PaletteSet, show_background_color=False) -> None:
        super().__init__(parent, palette_set, show_background_color)

    def _load_button(self) -> QWidget:
        def set_background_color(color):
            palette_set = self.palette_set
            palette_set[0][0] = color
            self.palette_set = palette_set

        button = ColorWidget.as_tiny(self, self.palette_set[0][0])
        button.update_observable.attach_observer(lambda color, *_: set_background_color(color))
        return button

    def _load_palette(self, idx: int) -> QWidget:
        def set_palette(palette):
            # Update the palette set to incorporate the new palette
            palette_set = self.palette_set
            palette_set[idx] = palette
            self.palette_set = palette_set

        button = PaletteWidget(self, self.palette_set[idx], False)
        button.update_observable.attach_observer(lambda palette, *_: set_palette(palette))
        return button


if __name__ == "__main__":
    # Loads a test widget to see how it works in isolation

    from PySide2.QtWidgets import QApplication, QMainWindow

    from foundry.core.Color.PaletteController import PaletteController
    from foundry.core.Palette.Palette import Palette

    palette_controller = PaletteController()

    pal = PaletteSet(
        Palette(
            palette_controller.colors[0],
            palette_controller.colors[1],
            palette_controller.colors[2],
            palette_controller.colors[3]
        ),
        Palette(
            palette_controller.colors[0],
            palette_controller.colors[4],
            palette_controller.colors[5],
            palette_controller.colors[6]
        ),
        Palette(
            palette_controller.colors[0],
            palette_controller.colors[7],
            palette_controller.colors[8],
            palette_controller.colors[9]
        ),
        Palette(
            palette_controller.colors[0],
            palette_controller.colors[10],
            palette_controller.colors[11],
            palette_controller.colors[12]
        )
    )

    app = QApplication()
    main_window = QMainWindow()
    main_window.setCentralWidget(PaletteSetEditorWidget(None, pal, True))
    main_window.showMaximized()
    app.exec_()

