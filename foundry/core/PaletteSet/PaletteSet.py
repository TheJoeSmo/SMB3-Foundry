

from dataclasses import dataclass

from ..Palette.Palette import Palette


@dataclass
class PaletteSet:
    """Defines a set of four palettes"""
    palette_0: Palette
    palette_1: Palette
    palette_2: Palette
    palette_3: Palette

    def __str__(self) -> str:
        return f"({self[0]}),({self[1]}),({self[2]}),({self[3]})"

    def __getitem__(self, item: int) -> Palette:
        if item == 0:
            return self.palette_0
        elif item == 1:
            return self.palette_1
        elif item == 2:
            return self.palette_2
        elif item == 3:
            return self.palette_3
        else:
            raise NotImplementedError

    def __setitem__(self, key: int, value: Palette):
        if key == 0:
            self.palette_0 = value
        elif key == 1:
            self.palette_1 = value
        elif key == 2:
            self.palette_2 = value
        elif key == 3:
            self.palette_3 = value
        else:
            raise NotImplementedError

    @classmethod
    def from_palette_set(cls, palette_set: "PaletteSet"):
        cls(palette_set.palette_0, palette_set.palette_1, palette_set.palette_2, palette_set.palette_3)

    @property
    def nes_str(self) -> str:
        """Defines the palette as a NES palette string"""
        return f"{self[0].nes_str},{self[1].nes_str},{self[2].nes_str},{self[3].nes_str}"
