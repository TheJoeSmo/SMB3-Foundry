

from typing import Callable

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin


class Plugin(AbstractPlugin):
    """
    A generic implementation of a Plugin.  This Plugin implements a real world way to instantiate plugins in a real
    context.
    """

    def __init__(
            self,
            name: str,
            create: Callable,
            delete: Callable,
            enable: Callable,
            disable: Callable
    ):
        super().__init__(name)
        self._create = create
        self._delete = delete
        self._enable = enable
        self._disable = disable

    def create(self) -> bool:
        return self._create()

    def delete(self) -> bool:
        return self._delete()

    def enable(self) -> bool:
        return self._enable()

    def disable(self) -> bool:
        return self._disable()
