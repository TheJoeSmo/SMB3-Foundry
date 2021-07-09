from typing import Dict
from abc import ABC

from core.FileManager.AbstractHandler import AbstractHandler


class HandlerKeyError(KeyError):
    """An extended key error, to provide additional information regarding the name searched and handler called"""
    def __init__(self, name: str, handler_dict):
        self.name = name
        self.handler_dict = handler_dict
        super().__init__()


class HandlerDict:
    """A specialized dict for handlers, that provides additional debug information and type hints"""
    def __init__(self, handlers: Dict[str, AbstractHandler], **kwargs) -> None:
        self._handlers = handlers

    def __getattr__(self, item: str) -> AbstractHandler:
        try:
            return self._handlers[item]
        except KeyError:
            raise HandlerKeyError(item, self)  # Provide additional information

    def __iter__(self):
        return iter(self._handlers)

    def keys(self):
        return self._handlers.keys()

    def items(self):
        return self._handlers.items()

    def values(self):
        return self._handlers.values()


class AbstractPassableHandler(AbstractHandler, ABC):
    def __init__(self, handlers: Dict[str, AbstractHandler]):
        self._handlers = HandlerDict(handlers)

    @property
    def handlers(self) -> HandlerDict:
        return self._handlers
