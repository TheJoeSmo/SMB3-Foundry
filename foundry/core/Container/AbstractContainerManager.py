from typing import List
from abc import ABC, abstractmethod

from foundry.core.Cursor.Cursor import Cursor

from .AbstractContainer import AbstractContainer
from ..Filler.Filler import Filler


class AbstractContainerManager(AbstractContainer, ABC):
    def __bytes__(self) -> bytes:
        if not self.safe_to_save:
            raise IndexError(
                f"{list(filter(self.filler_safe_to_save, self.fillers))} cannot be saved to bytes because they are not inside {self}"
            )

        b = bytearray(self.size)  # Fill in 0s by default
        for filler in self.fillers:
            b[filler.container_offset : filler.container_offset + filler.size] = bytes(filler)

        return bytes(b)

    @staticmethod
    @abstractmethod
    def filler_safe_to_save(filler: Filler) -> bool:
        """Returns if filler is safe to save"""

    @property
    @abstractmethod
    def safe_to_save(self) -> bool:
        """Returns if the container is safe to save"""

    @property
    @abstractmethod
    def fillers(self) -> List[Filler]:
        """Returns all the fillers of the container"""
