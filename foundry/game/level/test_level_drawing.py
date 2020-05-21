import os
from pathlib import Path

import pytest
from PySide2.QtCore import QPoint, QRect, QSize

from foundry import data_dir
from foundry.conftest import compare_images
from foundry.game.level.LevelRef import LevelRef
from foundry.gui.ContextMenu import ContextMenu
from foundry.gui.LevelView import LevelView
from smb3parse.levels import HEADER_LENGTH
from smb3parse.objects.object_set import WORLD_MAP_OBJECT_SET

reference_image_dir = Path(__file__).parent.joinpath("test_refs")
reference_image_dir.mkdir(parents=True, exist_ok=True)


def _test_level_against_reference(level_view: LevelView, qtbot):
    qtbot.addWidget(level_view)

    image_name = f"{level_view.level_ref.level.name}.png"
    ref_image_path = str(reference_image_dir.joinpath(image_name))

    level_view.repaint()

    compare_images(image_name, ref_image_path, level_view.grab())


def current_test_name():
    return os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].replace("/", "_")


level_data = []
test_name = []

with open(data_dir / "levels.dat", "r") as level_data_file:
    for line in level_data_file.readlines():
        world_no, level_no, level_address, enemy_address, object_set_number, level_name = line.strip().split(",")

        world_no = int(world_no)
        level_no = int(level_no)

        level_address = int(level_address, 16) - HEADER_LENGTH

        enemy_address = int(enemy_address, 16)

        object_set_number = int(object_set_number, 16)

        if object_set_number == WORLD_MAP_OBJECT_SET:
            continue

        level_data.append((world_no, level_no, level_address, enemy_address, object_set_number))
        test_name.append(f"Level {world_no}-{level_no} - {level_name}")


@pytest.mark.parametrize("level_info", level_data, ids=test_name)
def test_level(level_info, qtbot):
    level_ref = LevelRef()
    level_ref.load_level(*level_info)

    # monkeypatch level names, since the level name data is broken atm
    level_ref.level.name = current_test_name()

    level_view = LevelView(None, level_ref, ContextMenu(level_ref))
    level_view.transparency = True

    rect = QRect(QPoint(0, 0), QSize(*level_ref.level.size) * 16)

    level_view.setGeometry(rect)

    _test_level_against_reference(level_view, qtbot)
