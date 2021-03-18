

from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Observables.SilencerGenericObservable import SilencerGenericObservable
from foundry.core.Color.Color import Color
from foundry.core.Color.ObservableColor import ObservableColor
from foundry.core.Palette.Palette import Palette


def _color_getter(color_index):
    """A wrapper to make properties for color_0-3"""
    def color_getter(self: "ObservablePalette"):
        # Get the internal palette's color
        return self.palette[color_index]
    return color_getter


def _color_setter(color_index):
    """A wrapper to make properties for color_0-3"""
    def color_setter(self, color):
        self[color_index] = color
    return color_setter


class ObservablePalette(Palette):
    """A palette that emits an update when edited"""

    def __init__(self, color_0: Color, color_1: Color, color_2: Color, color_3: Color):
        # This makes it so the colors will automatically update if updates outside the class
        self._palette = Palette(
            c1 := ObservableColor.from_color(color_0),
            c2 := ObservableColor.from_color(color_1),
            c3 := ObservableColor.from_color(color_2),
            c4 := ObservableColor.from_color(color_3)
        )
        self.update_observable = GenericObservable("update")
        # Notifications will be silenced to avoid multiple calls
        self.palette_update_observable = SilencerGenericObservable("palette_update")
        for color in [c1, c2, c3, c4]:
            # Push the color update forward, note the color will stop the loop
            color.update_observable.attach_observer(
                lambda *_: self.palette_update_observable.notify_observers(self.palette)
            )
        self.palette_update_observable.notify_observers(lambda *_: self.update_observable.notify_observers())

    def __setitem__(self, key: int, color: Color):
        # Note, if you update the palette by setting it in a list, you will cause more updates
        # It is better to send a new palette, so only one update occurs
        palette = self.palette
        palette[key] = color
        self.palette = palette

    color_0 = property(fget=_color_getter(0), fset=_color_setter(0))
    color_1 = property(fget=_color_getter(1), fset=_color_setter(1))
    color_2 = property(fget=_color_getter(2), fset=_color_setter(2))
    color_3 = property(fget=_color_getter(3), fset=_color_setter(3))

    @property
    def palette(self) -> Palette:
        """Provide a copy of the palette"""
        return Palette(self._palette[0], self._palette[1], self._palette[2], self._palette[3])

    @palette.setter
    def palette(self, palette: Palette) -> None:
        # Only provide an update if something changes
        if palette != self.palette:
            # We do not want multiple updates, so we will pause it while we set each color
            self.palette_update_observable.silenced = True

            # We want to preserve the observable colors inside the palette, so we will manually transfer it
            for i in range(4):
                self._palette[i].color = palette[i]  # Push the new color into the observable color

            # Send the update manually because we silenced it
            self.palette_update_observable.silenced = False
            self.palette_update_observable.notify_observers(palette)
