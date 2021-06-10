from typing import Optional, List

from .AbstractContainer import AbstractContainer
from ..Address import determine_pc_offset, determine_rom_offset


class FloatingContainer(AbstractContainer):
    """
    A representation of a segment of data, that is substent in itself.
    """

    def __init__(
        self, name: Optional[str], rom_offset: int, pc_offset: int, size: int, children: List[AbstractContainer]
    ):
        self._name: str = name or ""
        self._rom_offset = rom_offset
        self._pc_offset = pc_offset
        self._size = size
        self._children = set(children)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, {self.rom_offset}, "
            f"{self.pc_offset}, {self.size}, {self.children})"
        )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def rom_offset(self) -> int:
        return self._rom_offset

    @rom_offset.setter
    def rom_offset(self, rom_offset: int):
        self._rom_offset = rom_offset
        self._pc_offset = determine_pc_offset(self.pc_offset, rom_offset)

    @property
    def pc_offset(self) -> int:
        return self._pc_offset

    @pc_offset.setter
    def pc_offset(self, pc_offset: int):
        self._pc_offset = pc_offset
        self._rom_offset = determine_rom_offset(pc_offset, self.rom_offset)

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def children(self) -> List[AbstractContainer]:
        return list(self._children)

    @children.setter
    def children(self, children: List[AbstractContainer]):
        self._children = set(children)

    def add_child(self, child: AbstractContainer):
        self._children.add(child)

    def remove_child(self, child: AbstractContainer):
        self._children.remove(child)
