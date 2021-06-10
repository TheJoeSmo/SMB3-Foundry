from typing import List
from abc import ABC, abstractmethod


class AbstractContainer(ABC):
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.rom_offset}, {self.pc_offset}, {self.size})"

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the container"""

    @property
    @abstractmethod
    def rom_offset(self) -> int:
        """The offset into the actual ROM of the container"""

    @property
    @abstractmethod
    def pc_offset(self) -> int:
        """The offset into the 16bit program counter of the ROM"""

    @property
    @abstractmethod
    def size(self) -> int:
        """The size the container requests"""

    @property
    @abstractmethod
    def children(self) -> List:
        """Anything that is inside the container"""

    @abstractmethod
    def add_child(self, child):
        """Adds a child to the list of the container's children"""

    @abstractmethod
    def remove_child(self, child):
        """Removes a child from the list of the container's children"""

    def remove_children(self):
        """Removes all the children used by the container"""
        for child in self.children:
            self.remove_child(child)
