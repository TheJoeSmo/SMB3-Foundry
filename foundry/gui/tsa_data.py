from typing import Optional
from os import path
from json import dump, load
from time import time

from PySide2.QtWidgets import QWidget, QFileDialog

from core.TileSquareAssembly import load_or_create_database, get_tsa_offset
from core.TileSquareAssembly.Saver.JSONROMConverter import rom_to_dict, dict_to_rom
from core.TileSquareAssembly.Saver.Controller import Controller
from foundry.game.File import ROM as File
from foundry.game.gfx.drawable.Block import clear_block_cache

JSON_FILE_FILTER = "JSON (*.json);;All files (*)"

controller: Optional[Controller] = None


def get_controller():
    return controller


_hashed_tsa_data = {}
_changes_time: Optional[float] = None


def get_tsa_data(tileset: int) -> bytes:
    global _hashed_tsa_data

    if controller.has_changes:
        global _changes_time
        if _changes_time is None:
            _changes_time = time() + 3
        elif time() > _changes_time:
            _changes_time = None
            clear_block_cache()
            _hashed_tsa_data = {}

    if tileset not in _hashed_tsa_data:
        tsa_offset = get_tsa_offset(tileset)
        for tsa in controller.rom.tile_square_assemblies:
            if int(tsa_offset) == int(tsa.tsa_offset):
                tsa_data = bytes(tsa.to_bytes())
                _hashed_tsa_data.update({tileset: tsa_data})
                break
    return _hashed_tsa_data[tileset]


def initialize(parent: QWidget, rom_name: str):
    global controller
    load_or_create_database()
    controller = Controller(parent, rom_name)


def import_tsa_data(parent: QWidget) -> bool:
    recommended_file = File.name
    if not recommended_file.endswith(".json"):
        recommended_file += ".json"

    pathname, _ = QFileDialog.getOpenFileName(parent, caption="Open ROM", filter=JSON_FILE_FILTER)
    if not pathname:
        return False

    with open(pathname, "r") as f:
        controller.import_new(dict_to_rom(load(f)))


def export_tsa_data(parent: QWidget) -> bool:
    if controller.has_changes:
        controller.save()

    recommended_file = f"{path.expanduser('~')}/{File.name}_tsa.json"

    pathname, _ = QFileDialog.getSaveFileName(
        parent, caption="Export TSA Data to JSON", dir=recommended_file, filter=JSON_FILE_FILTER
    )

    if not pathname:
        return False

    with open(pathname, "w+") as f:
        dump(rom_to_dict(controller.rom), f, indent=4)
