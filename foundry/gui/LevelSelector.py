from PySide6.QtCore import QMargins, QSize, Signal, SignalInstance
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QScrollBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from foundry import icon
from foundry.game.gfx.drawable.Block import Block
from foundry.game.level.Level import Level
from foundry.game.level.LevelRef import LevelRef
from foundry.game.level.WorldMap import WorldMap
from foundry.gui.Spinner import Spinner
from foundry.gui.WorldView import WorldView
from foundry.gui.settings import Settings
from smb3parse.constants import TILE_MUSHROOM_HOUSE_1, TILE_MUSHROOM_HOUSE_2, TILE_SPADE_HOUSE
from smb3parse.levels import FIRST_VALID_ROW, WORLD_COUNT
from smb3parse.objects.object_set import WORLD_MAP_OBJECT_SET

WORLD_ITEMS = [
    "World Maps",
    "World 1",
    "World 2",
    "World 3",
    "World 4",
    "World 5",
    "World 6",
    "World 7",
    "World 8",
    "Lost Levels",
]

OBJECT_SET_ITEMS = [
    "0 Overworld",
    "1 Plains",
    "2 Dungeon",
    "3 Hilly",
    "4 Sky",
    "5 Piranha Plant",
    "6 Water",
    "7 Mushroom",
    "8 Pipe",
    "9 Desert",
    "A Ship",
    "B Giant",
    "C Ice",
    "D Cloudy",
    "E Underground",
    "F Spade Bonus",
]


OVERWORLD_MAPS_INDEX = 0
WORLD_1_INDEX = 1


class LevelSelector(QDialog):
    def __init__(self, parent):
        super(LevelSelector, self).__init__(parent)

        self.setWindowTitle("Level Selector")
        self.setModal(True)

        self.level_name = ""

        self.object_set = 0
        self.world_index = 0
        self.object_data_offset = 0x0
        self.enemy_data_offset = 0x0

        self.world_label = QLabel(parent=self, text="World")
        self.world_list = QListWidget(parent=self)
        self.world_list.addItems(WORLD_ITEMS)

        self.world_list.itemDoubleClicked.connect(self.on_ok)
        self.world_list.itemSelectionChanged.connect(self.on_world_click)

        self.level_label = QLabel(parent=self, text="Level")
        self.level_list = QListWidget(parent=self)

        self.level_list.itemDoubleClicked.connect(self.on_ok)
        self.level_list.itemSelectionChanged.connect(self.on_level_click)

        self.enemy_data_label = QLabel(parent=self, text="Enemy Data")
        self.enemy_data_spinner = Spinner(parent=self)

        self.object_data_label = QLabel(parent=self, text="Object Data")
        self.object_data_spinner = Spinner(self)

        self.object_set_label = QLabel(parent=self, text="Object Set")
        self.object_set_dropdown = QComboBox(self)
        self.object_set_dropdown.addItems(OBJECT_SET_ITEMS)

        self.button_ok = QPushButton("Ok", self)
        self.button_ok.clicked.connect(self.on_ok)
        self.button_ok.setFocus()

        self.button_cancel = QPushButton("Cancel", self)
        self.button_cancel.clicked.connect(self.close)

        stock_level_widget = QWidget()
        stock_level_layout = QGridLayout(stock_level_widget)

        stock_level_layout.addWidget(self.world_label, 0, 0)
        stock_level_layout.addWidget(self.level_label, 0, 1)

        stock_level_layout.addWidget(self.world_list, 1, 0)
        stock_level_layout.addWidget(self.level_list, 1, 1)

        self.source_selector = QTabWidget()
        self.source_selector.addTab(stock_level_widget, "Stock Levels")
        self.source_selector.setTabIcon(0, icon("list.svg"))

        for world_number in range(WORLD_COUNT - 1):
            world_number += 1

            world_map_select = WorldMapLevelSelect(world_number)
            world_map_select.level_selected.connect(self._on_level_selected_via_world_map)

            self.source_selector.addTab(world_map_select, f"World {world_number}")
            self.source_selector.setTabIcon(world_number, icon("globe.svg"))

        # show world 1 by default
        if self.source_selector.count() > 1:
            self.source_selector.setCurrentIndex(1)

        data_layout = QGridLayout()

        data_layout.addWidget(self.enemy_data_label, 0, 0)
        data_layout.addWidget(self.object_data_label, 0, 1)
        data_layout.addWidget(self.enemy_data_spinner, 1, 0)
        data_layout.addWidget(self.object_data_spinner, 1, 1)

        data_layout.addWidget(self.object_set_label, 2, 0)
        data_layout.addWidget(self.object_set_dropdown, 2, 1)

        data_layout.addWidget(self.button_ok, 3, 0)
        data_layout.addWidget(self.button_cancel, 3, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.source_selector)
        main_layout.addLayout(data_layout)

        self.setLayout(main_layout)

        self.world_list.setCurrentRow(1)  # select Level 1-1
        self.on_world_click()

    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.key() == Qt.Key_Escape:
            self.reject()

    def on_world_click(self):
        index = self.world_list.currentRow()

        assert index >= 0

        self.level_list.clear()

        # skip first meaningless item
        for level in Level.offsets[1:]:
            if level.game_world == index:
                if level.name:
                    self.level_list.addItem(level.name)

        if self.level_list.count():
            self.level_list.setCurrentRow(0)

            self.on_level_click()

    def on_level_click(self):
        index = self.level_list.currentRow()

        assert index >= 0

        level_is_overworld = self.world_list.currentRow() == OVERWORLD_MAPS_INDEX

        if level_is_overworld:
            level_array_offset = index + 1
            self.level_name = ""
        else:
            level_array_offset = Level.world_indexes[self.world_list.currentRow()] + index + 1
            self.level_name = f"World {self.world_list.currentRow()}, "

        self.world_index = self.world_list.currentRow()

        self.level_name += f"{Level.offsets[level_array_offset].name}"

        object_data_for_lvl = Level.offsets[level_array_offset].rom_level_offset

        if not level_is_overworld:
            object_data_for_lvl -= Level.HEADER_LENGTH

        if not level_is_overworld:
            enemy_data_for_lvl = Level.offsets[level_array_offset].enemy_offset
        else:
            enemy_data_for_lvl = 0

        if enemy_data_for_lvl > 0:
            # data in look up table is off by one, since workshop ignores the first byte
            enemy_data_for_lvl -= 1

        self.enemy_data_spinner.setEnabled(not level_is_overworld)

        object_set_index = Level.offsets[level_array_offset].real_obj_set
        self.button_ok.setDisabled(level_is_overworld)

        self._fill_in_data(object_set_index, object_data_for_lvl, enemy_data_for_lvl)

    def _fill_in_data(self, object_set: int, layout_address: int, enemy_address: int):
        self.object_set_dropdown.setCurrentIndex(object_set)
        self.object_data_spinner.setValue(layout_address)
        self.enemy_data_spinner.setValue(enemy_address)

    def _on_level_selected_via_world_map(
        self, level_name: str, world_index: int, object_set: int, layout_address: int, enemy_address: int
    ):
        self.level_name = level_name

        self.world_index = world_index + 1

        self._fill_in_data(object_set, layout_address, enemy_address)

        self.on_ok()

    def on_ok(self, _=None):
        if self.world_list.currentRow() == OVERWORLD_MAPS_INDEX:
            return

        self.object_set = self.object_set_dropdown.currentIndex()
        self.object_data_offset = self.object_data_spinner.value()
        # skip the first byte, because it seems useless
        self.enemy_data_offset = self.enemy_data_spinner.value() + 1

        self.accept()

    def closeEvent(self, _close_event: QCloseEvent):
        self.reject()


class WorldMapLevelSelect(QScrollArea):
    level_selected: SignalInstance = Signal(str, int, int, int, int)

    def __init__(self, world_number: int):
        super(WorldMapLevelSelect, self).__init__()

        self.world = WorldMap.from_world_number(world_number)

        level_ref = LevelRef()
        level_ref.load_level("World", self.world.layout_address, 0x0, WORLD_MAP_OBJECT_SET)

        self.world_view = WorldView(self, level_ref, Settings(), None)

        self.world_view.setMouseTracking(True)
        self.world_view.draw_start = False
        self.world_view.read_only = True
        self.world_view.settings.setValue("world view/show level previews", True)
        self.world_view.zoom_in()

        self.setWidget(self.world_view)

        self.setMouseTracking(True)

    def mouseReleaseEvent(self, event: QMouseEvent):
        x, y = self.world_view.mapFromParent(event.pos()).toTuple()

        x //= Block.WIDTH * self.world_view.zoom
        y //= Block.HEIGHT * self.world_view.zoom

        y += FIRST_VALID_ROW

        try:
            level_pointer = self.world.level_pointer_at(x, y)

            if level_pointer is None:
                return

            if self.world.tile_at(x, y) in [TILE_SPADE_HOUSE, TILE_MUSHROOM_HOUSE_1, TILE_MUSHROOM_HOUSE_2]:
                QMessageBox.warning(
                    self, "No can do", "Spade and mushroom house currently not supported, when getting a level address."
                )
                return

            # todo change to emitting the level pointer
            self.level_selected.emit(
                self.world.level_name_at_position(x, y),
                self.world.internal_world_map.world_index,
                level_pointer.data.object_set,
                level_pointer.data.level_address,
                level_pointer.data.enemy_address,
            )
        except ValueError:
            pass

    def sizeHint(self) -> QSize:
        orig_size = super(WorldMapLevelSelect, self).sizeHint()

        scrollbar_width = QScrollBar().sizeHint().width()

        return orig_size.grownBy(QMargins(scrollbar_width, scrollbar_width, 0, 0))
