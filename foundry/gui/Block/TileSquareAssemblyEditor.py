

import yaml
from yaml import CLoader as Loader
from copy import copy
from typing import Optional
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWhatsThis, QSizePolicy
from PySide2.QtCore import QSize

from foundry import icon, data_dir

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Size.Size import Size

from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.gui.ChildWindow.ChildWindow import ChildWindow
from foundry.gui.QToolbar.Toolbar import Toolbar
from foundry.gui.PaletteSet.PaletteSetEditorWidget import PaletteSetEditorWidget
from foundry.gui.Block.BlockEditor import BlockEditor
from foundry.core.Block.Block import Block
from foundry.gui.PatternTable.TilesetPatternTableWidget import TilesetPatternTableWidget
from foundry.gui.Panel.Panel import Panel

from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler

from foundry.gui.Block.TileSquareAssemblyPicker import TileSquareAssemblyPicker

with open(data_dir.joinpath("tileset_info.yaml")) as f:
    tilesets = yaml.load(f, Loader=Loader)

tileset_offsets = [tileset["C000"] for tileset in tilesets.values()]
tileset_offsets[0] = 12  # correct incorrect world offset


class TileSquareAssemblyEditor(ChildWindow):
    """The viewer of the TSA editor"""

    def __init__(
            self,
            parent,
            tileset: int,
            palette_set: PaletteSet,
            zoom: Optional[Size] = None,
            block_selected: int = 0,
            title: Optional[str] = None
    ):
        super().__init__(parent, title if title is not None else "Tile Square Assembly Editor")

        self._zoom = zoom if zoom is not None else Size(1, 1)
        self._transparency = False

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.create_toolbar()

        self.update_observable = GenericObservable("update")
        self.size_update_observable = GenericObservable("size_update")

        # Index for the block currently selected
        self.block_currently_selected_observable = GenericObservable("block_selected_update")
        self.block_currently_selected = block_selected

        # Pattern table widget and updates
        self.pattern_table_update_observable = GenericObservable("pattern_table_update")
        self.tileset_update_observable = GenericObservable("tileset_update")
        self.tileset_update_observable.attach_observer(lambda *args: print("tileset", *args))
        self.pattern_table_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.pattern_table_widget = TilesetPatternTableWidget(self, tileset)
        self._tsa_data = ROM().get_tsa_data(tileset)
        self.pattern_table_widget.update_observable.attach_observer(
            lambda *_: self.pattern_table_update_observable.notify_observers(
                self.pattern_table_widget.pattern_table
            )
        )
        self.pattern_table_widget.update_observable.attach_observer(self.tileset_update_observable.notify_observers)

        # Whenever the pattern table changes, the tsa needs to as well
        def update_tsa_data_from_pattern_table(pattern_table_handler: PatternTableHandler):
            self._tsa_data = pattern_table_handler.data
            self.tsa_data_observable.notify_observers(self.tsa_data)
        self.pattern_table_update_observable.attach_observer(update_tsa_data_from_pattern_table)

        self.tileset_toolbar = Toolbar.default_toolbox(
            self, "tileset_toolbar", Panel(self, "Tileset", self.pattern_table_widget), Qt.RightToolBarArea
        )

        # Palette set widget and updates
        self.palette_set_update_observable = GenericObservable("palette_set_update")
        self.palette_set_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())
        self.palette_set_editor = PaletteSetEditorWidget(self, palette_set, True)
        self.palette_set_toolbox = Toolbar.default_toolbox(
            self, "palette_set_toolbox", self.palette_set_editor, Qt.RightToolBarArea
        )
        self.palette_set_editor.update_observable.attach_observer(
            lambda *_: self.palette_set_update_observable(self.palette_set_editor.palette_set)
        )

        # Block editing widget and tsa data updates
        self.tsa_data_observable = GenericObservable("tsa_data_update")

        self.edited_block = Block(
            Size(self.zoom.width * 3, self.zoom.height * 3),
            self.block_currently_selected,
            self.pattern_table,
            self.palette_set,
            self.tsa_data,
            self.transparency
        )

        self.block_editor = BlockEditor(self, self.edited_block)
        self.block_editor.tsa_data_update_observable.attach_observer(lambda d: setattr(self, "tsa_data", d))

        def update_selected_block(index: int):
            self.block_editor.index = index
        self.block_currently_selected_observable.attach_observer(update_selected_block)

        def update_pattern_table(pattern_table: PatternTableHandler):
            self.block_editor.pattern_table.pattern_table = pattern_table.pattern_table
        self.pattern_table_update_observable.attach_observer(update_pattern_table)

        def update_palette_set(palette_set: PaletteSet):
            self.edited_block.palette_set = palette_set
        self.palette_set_update_observable.attach_observer(update_palette_set)

        def update_tsa_data(tsa_data: bytearray):
            self.edited_block.tsa_data = tsa_data
        self.tsa_data_observable.attach_observer(update_tsa_data)

        def update_zoom(size):
            self.edited_block.size = Size(size.width * 3, size.height * 3)
        self.size_update_observable.attach_observer(update_zoom)

        self.block_editor_toolbox = Toolbar.default_toolbox(
            self, "block_editor_toolbar", self.block_editor, Qt.RightToolBarArea
        )

        self.tsa_viewer = TileSquareAssemblyPicker(self, self.palette_set, self.tileset, self.zoom)

        def set_block_selected(selected: int):
            self.block_currently_selected = selected
        self.tsa_viewer.block_selected_update_observable.attach_observer(set_block_selected)

        def update_tileset(tileset: int):
            self.tsa_viewer.tileset = tileset
        self.tileset_update_observable.attach_observer(update_tileset)

        def update_viewer_palette_set(palette_set: PaletteSet):
            self.tsa_viewer.palette_set = palette_set
        self.palette_set_update_observable.attach_observer(update_viewer_palette_set)

        self.setCentralWidget(self.tsa_viewer)

        self.setWhatsThis(
            "<b>Tile Square Assembly Editor</b>"
            "<br/>"
            "An editor for the 256 16x16 pixel blocks in a given tileset."
            "<br/>"
        )
        self.showNormal()

    @property
    def block_currently_selected(self) -> int:
        return self._block_currently_selected

    @block_currently_selected.setter
    def block_currently_selected(self, selected: int) -> None:
        self._block_currently_selected = selected
        self.block_currently_selected_observable.notify_observers(selected)

    @property
    def tsa_data(self) -> bytearray:
        return copy(self._tsa_data)

    @tsa_data.setter
    def tsa_data(self, tsa_data: bytearray) -> None:
        if self._tsa_data != tsa_data:
            # We do not want to end up having the same tsa everywhere, so we must copy it
            self._tsa_data = copy(tsa_data)
            self.tsa_data_observable.notify_observers(copy(self._tsa_data))

    @property
    def transparency(self) -> bool:
        return self._transparency

    @transparency.setter
    def transparency(self, transparency: bool) -> None:
        self._transparency = transparency

    @property
    def zoom(self) -> Size:
        """The size of the blocks displayed"""
        return self._zoom

    @zoom.setter
    def zoom(self, zoom: Size) -> None:
        if zoom != self.zoom:
            self._zoom = zoom
            self.size_update_observable.notify_observers(zoom)

    @property
    def palette_set(self) -> PaletteSet:
        """The palette set used by the editor"""
        return self.palette_set_editor.palette_set

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self.palette_set_editor.palette_set = palette_set

    @property
    def tileset(self) -> int:
        """The tileset of the current tsa"""
        return self.pattern_table_widget.currentIndex()

    @tileset.setter
    def tileset(self, tileset: int) -> None:
        if self.tileset != tileset:
            self.pattern_table_widget.setCurrentIndex(tileset)

    @property
    def offset(self) -> int:
        """The offset to the bank for the tsa"""
        return tileset_offsets[self.tileset]

    @property
    def pattern_table(self) -> PatternTableHandler:
        """The pattern table of the tsa"""
        return self.pattern_table_widget.pattern_table

    def create_toolbar(self):
        menu_toolbar = Toolbar("Menu Toolbar", self)
        menu_toolbar.setOrientation(Qt.Horizontal)
        menu_toolbar.setIconSize(QSize(20, 20))

        self.save_file_action = menu_toolbar.addAction(icon("save.svg"), "Save TSA")
        self.save_file_action.triggered.connect(lambda *_: self.save())
        self.save_file_action.setWhatsThis(
            "<b>Save TSA</b><br/>"
            "Saves the TSA to the ROM currently loaded<br/>"
        )
        menu_toolbar.addSeparator()

        self.zoom_out_action = menu_toolbar.addAction(icon("zoom-out.svg"), "Zoom Out")
        self.zoom_out_action.triggered.connect(
            lambda *_: setattr(self, "zoom", min(10, Size(self.zoom.width + 1, self.zoom.height + 1)))
        )
        self.zoom_out_action.setWhatsThis(
            "<b>Zoom Out</b><br/>"
            "Retracts the size of the Tile Square Assembly Editor<br/>"
        )
        self.zoom_in_action = menu_toolbar.addAction(icon("zoom-in.svg"), "Zoom In")
        self.zoom_in_action.triggered.connect(
            lambda *_: setattr(self, "zoom", Size(self.zoom.width - 1, self.zoom.height - 1))
        )
        self.zoom_in_action.setWhatsThis(
            "<b>Zoom In</b><br/>"
            "Expands the size of the Tile Square Assembly Editor<br/>"
        )

        menu_toolbar.addSeparator()

        whats_this_action = QWhatsThis.createAction()
        whats_this_action.setWhatsThis(
            "<b>What is This</b><br/>"
            "Provides an expanded tooltip of what a widget does whenever clicked on<br/>"
        )
        whats_this_action.setIcon(icon("help-circle.svg"))
        whats_this_action.setText("Starts 'What's this?' mode")
        menu_toolbar.addAction(whats_this_action)

        self.addToolBar(Qt.TopToolBarArea, menu_toolbar)

    def save(self) -> None:
        """Saves to the current rom"""
        ROM().bulk_write(self.tsa_data, (self.offset * 0x2000) + 0x10)
        ROM().save_to_file(ROM().path)


if __name__ == "__main__":
    # Loads a test widget to see how it works in isolation

    from PySide2.QtWidgets import QApplication, QMainWindow

    from foundry.core.Color.PaletteController import PaletteController
    from foundry.core.Palette.Palette import Palette

    from foundry import root_dir
    from foundry.game.File import ROM

    rom_path = root_dir.joinpath("SMB3.nes")
    ROM(rom_path)

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
    main_window.setCentralWidget(TileSquareAssemblyEditor(None, 0, pal))
    main_window.showNormal()
    app.exec_()
