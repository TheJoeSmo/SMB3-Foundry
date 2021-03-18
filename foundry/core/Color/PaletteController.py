

from typing import Optional
import yaml
from yaml import CLoader

from PySide2.QtGui import QColor

from foundry import root_dir
from .Color import Color

palette_file = root_dir.joinpath("data", "palette.yaml")

_NES_PAL_CONTROLLER = None


def _load_nes_colors():
    with open(palette_file) as f:
        d = yaml.load(f, Loader=CLoader)
    return {idx: (c["red"], c["green"], c["blue"]) for idx, c in enumerate(d)}


def _load_nes_colors_inverse():
    with open(palette_file) as f:
        d = yaml.load(f, Loader=CLoader)
    return {(c["red"], c["green"], c["blue"]): idx for idx, c in enumerate(d)}


class PaletteController:
    """A singleton that contains important NES palette information"""
    def __new__(cls, *args, **kwargs) -> "PaletteController":
        global _NES_PAL_CONTROLLER
        if _NES_PAL_CONTROLLER is None:
            _NES_PAL_CONTROLLER = super().__new__(cls, *args, **kwargs)
            _NES_PAL_CONTROLLER.colors = _load_nes_colors()
            _NES_PAL_CONTROLLER.colors_inverse = _load_nes_colors_inverse()
        return _NES_PAL_CONTROLLER

    def get_qcolor(self, color_idx: int) -> QColor:
        """Converts the color to a qcolor"""
        return QColor(self.colors[color_idx][0], self.colors[color_idx][1], self.colors[color_idx][2])

    def get_index_from_color(self, color: Color) -> Optional[int]:
        """Provides an approximate index for a given color into the NES palette"""
        for i, c in enumerate(self.colors.values()):
            if c == color:
                return i
        return None
