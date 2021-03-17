

from foundry.core.Size.Size import Size
from foundry.core.Observables.GenericObservable import GenericObservable


class ObservableSize(Size):
    """A size that is observable"""

    def __init__(self, width: int, height: int):
        self._size = Size(width, height)
        self.update_observable = GenericObservable("update")
        self.size_update_observable = GenericObservable("size_update")
        self.size_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

    @property
    def width(self) -> int:
        return self._size.width

    @width.setter
    def width(self, width: int) -> None:
        self.size = Size(width, self.height)

    @property
    def height(self) -> int:
        return self._size.height

    @height.setter
    def height(self, height: int)-> None:
        self.size = Size(self.width, height)
    
    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    @size.setter
    def size(self, size: Size) -> None:
        self._size = size
        self.size_update_observable.notify_observers(self.size)
