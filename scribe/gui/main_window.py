from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox, QScrollArea

from foundry.game.File import ROM
from foundry.game.level.LevelRef import LevelRef
from foundry.gui.MainWindow import ROM_FILE_FILTER
from foundry.gui.WorldView import WorldView
from scribe.gui.tool_window.tool_window import ToolWindow
from scribe.gui.world_view_context_menu import WorldContextMenu
from smb3parse.levels import WORLD_COUNT
from smb3parse.levels.world_map import WorldMap as SMB3WorldMap
from smb3parse.objects.object_set import WORLD_MAP_OBJECT_SET


class MainWindow(QMainWindow):
    def __init__(self, path_to_rom: str):
        super(MainWindow, self).__init__()

        self.level_ref = LevelRef()
        self.world = None

        self.on_open_rom(path_to_rom)

        self.world_view = WorldView(self, self.level_ref, WorldContextMenu(self.level_ref))
        self.world_view.zoom_in()
        self.world_view.zoom_in()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.world_view)

        self._setup_file_menu()
        self._setup_edit_menu()
        self._setup_view_menu()
        self._setup_level_menu()

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.edit_menu)
        self.menuBar().addMenu(self.view_menu)
        self.menuBar().addMenu(self.level_menu)

        self.setCentralWidget(self.scroll_area)

        self.tool_window = ToolWindow(self, self.level_ref)
        self.tool_window.tile_selected.connect(self.world_view.on_put_tile)

        self.show()
        self.tool_window.show()

    def _setup_file_menu(self):
        self.file_menu = QMenu("File")
        self.file_menu.triggered.connect(self.on_file_menu)

        self.open_rom_action = self.file_menu.addAction("Open ROM...")
        self.save_rom_action = self.file_menu.addAction("Save ROM")
        self.save_as_rom_action = self.file_menu.addAction("Save ROM As...")
        self.file_menu.addSeparator()
        self.quit_rom_action = self.file_menu.addAction("Quit")

    def _setup_edit_menu(self):
        self.edit_menu = QMenu("Edit")
        self.edit_menu.triggered.connect(self.on_edit_menu)

        self.delete_tiles_action = self.edit_menu.addAction("Delete All Tiles")
        self.delete_level_pointers_action = self.edit_menu.addAction("Delete All Level Pointers")
        self.delete_sprites_action = self.edit_menu.addAction("Delete All Sprites")

    def _setup_view_menu(self):
        self.view_menu = QMenu("View")
        self.view_menu.triggered.connect(self.on_view_menu)

        self.level_pointer_action = self.view_menu.addAction("Show Level Pointers")
        self.level_pointer_action.setCheckable(True)
        self.level_pointer_action.setChecked(self.world_view.draw_level_pointers)

        self.sprite_action = self.view_menu.addAction("Show Overworld Sprites")
        self.sprite_action.setCheckable(True)
        self.sprite_action.setChecked(self.world_view.draw_sprites)

        self.starting_point_action = self.view_menu.addAction("Show Starting Point")
        self.starting_point_action.setCheckable(True)
        self.starting_point_action.setChecked(self.world_view.draw_start)

    def _setup_level_menu(self):
        self.level_menu = QMenu("Change Level")
        self.level_menu.triggered.connect(self.on_level_menu)

        level_menu_action_group = QActionGroup(self)

        for level_index in range(WORLD_COUNT):
            action = self.level_menu.addAction(f"World {level_index + 1}")
            action.setCheckable(True)

            level_menu_action_group.addAction(action)

        self.level_menu.actions()[0].trigger()

    def on_open_rom(self, path_to_rom="") -> bool:
        if not path_to_rom:
            # otherwise ask the user what new file to open
            path_to_rom, _ = QFileDialog.getOpenFileName(self, caption="Open ROM", filter=ROM_FILE_FILTER)

            if not path_to_rom:
                return False

        # Proceed loading the file chosen by the user
        try:
            ROM.load_from_file(path_to_rom)
        except IOError as exp:
            QMessageBox.warning(self, type(exp).__name__, f"Cannot open file '{path_to_rom}'.")
            return False

    def load_level(self, world_number: int):
        self.world = SMB3WorldMap.from_world_number(ROM(), world_number)

        self.level_ref.load_level("World", self.world.layout_address, 0x0, WORLD_MAP_OBJECT_SET)

    def on_save_rom(self, is_save_as=False):
        if is_save_as:
            suggested_file = ROM.name

            if not suggested_file.endswith(".nes"):
                suggested_file += ".nes"

            pathname, _ = QFileDialog.getSaveFileName(
                self, caption="Save ROM as", dir=suggested_file, filter=ROM_FILE_FILTER
            )
            if not pathname:
                return  # the user changed their mind
        else:
            pathname = ROM.path

        self._save_current_changes_to_file(pathname, set_new_path=True)

        if not is_save_as:
            self.level_ref.level.changed = False
            self.level_ref.data_changed.emit()

    def _save_current_changes_to_file(self, pathname: str, set_new_path):
        self.level_ref.save_to_rom()

        try:
            ROM().save_to_file(pathname, set_new_path)
        except IOError as exp:
            QMessageBox.warning(self, f"{type(exp).__name__}", f"Cannot save ROM data to file '{pathname}'.")

    def on_file_menu(self, action: QAction):
        if action is self.open_rom_action:
            self.on_open_rom()
            self.load_level(1)
        elif action is self.save_rom_action:
            self.on_save_rom(False)
        elif action is self.save_as_rom_action:
            self.on_save_rom(True)
        elif action is self.quit_rom_action:
            self.close()

        self.world_view.update()

    def on_edit_menu(self, action: QAction):
        if action is self.delete_tiles_action:
            self.level_ref.level.remove_all_tiles()
        elif action is self.delete_sprites_action:
            self.level_ref.level.remove_all_sprites()

        self.world_view.update()

    def on_view_menu(self, action: QAction):
        if action is self.level_pointer_action:
            self.world_view.draw_level_pointers = action.isChecked()
        elif action is self.sprite_action:
            self.world_view.draw_sprites = action.isChecked()
        elif action is self.starting_point_action:
            self.world_view.draw_start = action.isChecked()

        self.world_view.update()

    def on_level_menu(self, action: QAction):
        self.load_level(self.level_menu.actions().index(action) + 1)

        if not self.isMaximized():
            self.resize(self.sizeHint())

    def sizeHint(self) -> QSize:
        inner_width, inner_height = self.world_view.sizeHint().toTuple()

        height = inner_height + self.scroll_area.horizontalScrollBar().height() + 2 * self.scroll_area.frameWidth()
        height += self.menuBar().height()

        width = inner_width + 2 * self.scroll_area.frameWidth()

        size_hint = QSize(min(width, QApplication.primaryScreen().size().width()), height)

        return size_hint