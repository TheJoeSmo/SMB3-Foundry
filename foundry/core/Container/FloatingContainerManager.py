from typing import Optional, List

from .AbstractContainer import AbstractContainer
from .AbstractContainerManager import AbstractContainerManager
from .FloatingContainer import FloatingContainer
from ..Filler.Filler import Filler


class FloatingContainerManager(FloatingContainer, AbstractContainerManager):
    def __init__(
        self, name: Optional[str], rom_offset: int, pc_offset: int, size: int, children: List[AbstractContainer]
    ):
        super().__init__(name, rom_offset, pc_offset, size, children)
        self._fillers = set()

    @staticmethod
    def filler_safe_to_save(filler: Filler) -> bool:
        return filler.inside_container

    @property
    def safe_to_save(self) -> bool:
        return all([filler.inside_container for filler in self.fillers])

    @property
    def fillers(self) -> List[Filler]:
        return list(self._fillers)

    @fillers.setter
    def fillers(self, fillers: List[Filler]):
        self._fillers = set(fillers)

    def add_child(self, filler: Filler):
        self._fillers.add(filler)

    def remove_child(self, filler: Filler):
        self._fillers.remove(filler)
