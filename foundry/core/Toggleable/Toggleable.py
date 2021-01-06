

from typing import Optional, Callable

from foundry.core.Toggleable.AbstractToggleable import AbstractToggleable


class Toggleable(AbstractToggleable):
    """
    A basic implementation of what a Toggleable should do
    Toggleable uses dependency injection for its enable and disable
    """

    def __init__(self, enable: Callable, disable: Callable, state: Optional[bool] = None, *args, **kwargs) -> None:
        self._enable = enable
        self._disable = disable
        super().__init__(state=state)

    def enable(self, *args, **kwargs) -> bool:
        return self._enable(*args, **kwargs)

    def disable(self, *args, **kwargs) -> bool:
        return self._disable(*args, **kwargs)
