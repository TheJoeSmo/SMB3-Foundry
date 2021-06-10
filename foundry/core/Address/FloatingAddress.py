from typing import Optional

from .AbstractAddress import AbstractAddress
from ..Container.AbstractContainer import AbstractContainer


class FloatAddress(AbstractAddress):
    def __init__(self, name: Optional[str], container: AbstractContainer, container_offset: int):
        self._name = name or ""
        self._container = container
        self._container_offset = container_offset

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.container}, {self.container_offset})"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def container(self) -> AbstractContainer:
        return self._container

    @container.setter
    def container(self, container: AbstractContainer):
        self._container = container

    @property
    def container_offset(self) -> int:
        return self._container_offset

    @container_offset.setter
    def container_offset(self, offset: int):
        self._container_offset = offset
