

from typing import Optional
from dataclasses import dataclass

from ..util.hexify import hexify


@dataclass
class Color:
    """Defines a color with a red, green, and blue value"""
    red: int
    green: int
    blue: int

    def __str__(self) -> str:
        return f"{self.red}, {self.green}, {self.blue}"

    @property
    def nes_index(self) -> Optional[int]:
        """Returns the estimated index of the color in terms of the NES palette"""
        from PaletteController import PaletteController
        return PaletteController().get_index_from_color(self)

    @property
    def nes_str(self) -> str:
        """Returns the color as a NES string"""
        return hexify(self.nes_index)
