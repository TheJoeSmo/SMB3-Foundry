

from typing import Optional

from ..Observables.GenericObservable import GenericObservable
from .Color import Color


class ObservableColor:
    """
    A color that emits an update when edited
    """

    def __init__(self, red: int, green: int, blue: int):
        self._color = Color(red, green, blue)
        self.update_action = GenericObservable("color_update")

    def __str__(self) -> str:
        return self._color.__str__()

    @classmethod
    def from_color(cls, color: Color):
        """Generates a ObservableColor from a color"""
        return cls(color.red, color.green, color.blue)

    @property
    def nes_index(self) -> Optional[int]:
        """Returns the estimated index of the color in terms of the NES palette"""
        return self._color.nes_index

    @property
    def nes_str(self) -> str:
        """Returns the color as a NES string"""
        return self._color.nes_str

    @property
    def red(self) -> int:
        return self._color.red

    @red.setter
    def red(self, color: int) -> None:
        self.color = Color(color, self.green, self.blue)

    @property
    def green(self) -> int:
        return self._color.green

    @green.setter
    def green(self, color: int) -> None:
        self.color = Color(self.red, color, self.blue)

    @property
    def blue(self) -> int:
        return self._color.blue

    @blue.setter
    def blue(self, color: int) -> None:
        self.color = Color(self.red, self.green, color)

    @property
    def color(self) -> Color:
        """The actual color being stored"""
        return Color(self.red, self.green, self.blue)  # Promote not mutating the value directly

    @color.setter
    def color(self, color: Color) -> None:
        self._color = color
        if len(self.update_action.observers):
            self.update_action.notify_observers(color)
