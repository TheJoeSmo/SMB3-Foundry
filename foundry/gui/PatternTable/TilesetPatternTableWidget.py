

from typing import Optional
import yaml
from yaml import CLoader
from PySide2.QtWidgets import QWidget

from foundry import data_dir

from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler

from foundry.gui.QComboBox.ComboBox import ComboBox, ComboBoxOption

with open(data_dir.joinpath("tileset_info.yaml")) as f:
    _tileset_info = yaml.load(f, Loader=CLoader)


class TilesetPatternTableWidget(ComboBox):
    """Provides a dropdown to select a tileset for a pattern table"""
    def __init__(self, parent: Optional[QWidget], tileset: int = 0):
        self.pattern_table = PatternTableHandler(PatternTable.from_tileset(tileset))
        super().__init__(
            parent, [ComboBoxOption(_tileset_info[i]["name"], self.update_pattern_table(i)) for i in _tileset_info]
        )
        self.setCurrentIndex(tileset)

    def update_pattern_table(self, tileset: int):
        self.pattern_table.pattern_table = PatternTable.from_tileset(tileset)


if __name__ == "__main__":
    # Loads a test widget to see how it works in isolation

    from PySide2.QtWidgets import QApplication, QMainWindow

    from foundry import root_dir
    from foundry.game.File import ROM

    rom_path = root_dir.joinpath("SMB3.nes")
    ROM(rom_path)

    app = QApplication()
    main_window = QMainWindow()
    main_window.setCentralWidget(TilesetPatternTableWidget(None, 0))
    main_window.showNormal()
    app.exec_()
