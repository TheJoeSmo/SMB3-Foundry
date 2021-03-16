

from dataclasses import dataclass

from ..Color.Color import Color


@dataclass
class Palette:
    """Defines a basic palette"""
    color_0: Color
    color_1: Color
    color_2: Color
    color_3: Color

    def __str__(self) -> str:
        return f"({self[0]}),({self[1]}),({self[2]}),({self[3]})"

    def __getitem__(self, item: int) -> Color:
        if item == 0:
            return self.color_0
        elif item == 1:
            return self.color_1
        elif item == 2:
            return self.color_2
        elif item == 3:
            return self.color_3
        else:
            raise NotImplementedError

    def __setitem__(self, key: int, value: Color):
        if key == 0:
            self.color_0 = value
        elif key == 1:
            self.color_1 = value
        elif key == 2:
            self.color_2 = value
        elif key == 3:
            self.color_3 = value
        else:
            raise NotImplementedError

    @classmethod
    def from_palette(cls, palette: "Palette"):
        """Generates a Palette from a Palette"""
        return cls(palette.color_0, palette.color_1, palette.color_2, palette.color_3)

    @property
    def nes_str(self) -> str:
        """Defines the palette as a NES palette string"""
        return f"{self[0].nes_str},{self[1].nes_str},{self[2].nes_str},{self[3].nes_str}"
