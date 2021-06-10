from abc import ABC, abstractmethod

from ..Container.AbstractContainer import AbstractContainer


class AbstractAddress(ABC):
    """
    A representation of an index inside a container.
    """

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.container}, {self.container_offset})"

    @property
    def inside_container(self) -> bool:
        return self.container.size > self.container_offset

    @property
    def space_remaining(self) -> int:
        return self.container.size - self.container_offset

    @property
    def rom_offset(self) -> int:
        return self.container.rom_offset + self.container_offset

    @rom_offset.setter
    def rom_offset(self, rom_offset: int):
        self.container_offset = rom_offset - self.container.rom_offset

    @property
    def pc_offset(self) -> int:
        return self.container.pc_offset + self.container_offset

    @pc_offset.setter
    def pc_offset(self, pc_offset: int):
        self.container_offset = pc_offset - self.container.pc_offset

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the address"""

    @property
    @abstractmethod
    def container(self) -> AbstractContainer:
        """The container that the address is housed inside"""

    @property
    @abstractmethod
    def container_offset(self) -> int:
        """The offset in which the address is located inside the container"""

    @container_offset.setter
    @abstractmethod
    def container_offset(self, offset: int):
        pass
