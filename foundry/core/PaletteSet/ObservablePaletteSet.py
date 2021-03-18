from foundry.core.Observables.GenericObservable import GenericObservable
from foundry.core.Observables.SilencerGenericObservable import SilencerGenericObservable
from foundry.core.Palette.ObservablePalette import ObservablePalette
from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Palette.Palette import Palette


def _palette_getter(palette_index):
    """A wrapper to make properties for palette_0-3"""
    def palette_getter(self):
        # Get the internal palette_set's palette
        return self.palette_set[palette_index]
    return palette_getter


def _palette_setter(palette_index):
    """A wrapper to make properties for palette_0-3"""
    def palette_setter(self, palette):
        self[palette_index] = palette
    return palette_setter


class ObservablePaletteSet(PaletteSet):
    """A palette set that emits an update when edited"""

    def __init__(self, palette_0: Palette, palette_1: Palette, palette_2: Palette, palette_3: Palette):
        # This makes it so the palettes will automatically update if it updates outside the class
        self._palette_set = PaletteSet(
            p1 := ObservablePalette.from_palette(palette_0),
            p2 := ObservablePalette.from_palette(palette_1),
            p3 := ObservablePalette.from_palette(palette_2),
            p4 := ObservablePalette.from_palette(palette_3)
        )

        self.update_observable = GenericObservable("update")
        # Notifications will be silenced to avoid multiple calls
        self.palette_set_update_observable = SilencerGenericObservable("palette_update")
        for palette in [p1, p2, p3, p4]:
            # Push the color update forward, note the color will stop the loop
            palette.update_observable.attach_observer(
                lambda *_: self.palette_set_update_observable.notify_observers(self.palette_set)
            )
        self.palette_set_update_observable.notify_observers(lambda *_: self.update_observable.notify_observers())

    def __setitem__(self, key: int, palette: Palette):
        # Note, if you update the palette set by setting it in a list, you will cause more updates
        # It is better to send a new palette set, so only one update occurs
        palette_set = self.palette_set
        palette_set[key] = palette
        self.palette_set = palette_set

    palette_0 = property(fget=_palette_getter(0), fset=_palette_setter(0))
    palette_1 = property(fget=_palette_getter(1), fset=_palette_setter(1))
    palette_2 = property(fget=_palette_getter(2), fset=_palette_setter(2))
    palette_3 = property(fget=_palette_getter(3), fset=_palette_setter(3))

    @property
    def palette_set(self) -> PaletteSet:
        """
        This provides a full copy of the palette set.  Even the colors will not refer to the actual palette.
        """
        return PaletteSet(self._palette_set[0], self._palette_set[1], self._palette_set[2], self._palette_set[3])

    @palette_set.setter
    def palette_set(self, palette_set: PaletteSet) -> None:
        self._palette_set = palette_set
        self.update_observable(palette_set)

        # Only provide an update if something changes
        if palette_set != self.palette_set:
            # We do not want multiple updates, so we will pause it while we set each palette
            self.palette_set_update_observable.silenced = True

            # We want to preserve the observable colors inside the palette set, so we will manually transfer it
            for i, palette in enumerate(palette_set):
                self._palette_set[i].palette = palette  # Push the new palette into the observable palette

            # Send the update manually because we silenced it
            self.palette_set_update_observable.silenced = False
            self.palette_set_update_observable.notify_observers(palette_set)
