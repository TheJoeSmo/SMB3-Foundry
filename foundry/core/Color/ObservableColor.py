

from typing import Union, Tuple

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Color.Color import Color


class ObservableColor(Color):
    """
    A color that emits an update when edited
    """

    def __init__(self, red: int, green: int, blue: int):
        self._color = Color(red, green, blue)

        self.update_observable = GenericObservable("update")
        self.color_update_observable = GenericObservable("color_update")
        self.color_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

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
    def color(self, color: Union[Color, Tuple[int, int, int]]) -> None:
        # Only update if needed
        if self._color != color:
            # Convert to a color if we we gave it a tuple instead of a color
            if isinstance(color, tuple):
                self._color = Color(color[0], color[1], color[2])
            else:
                self._color = Color(color.red, color.green, color.blue)
            self.color_update_observable.notify_observers(self.color)
