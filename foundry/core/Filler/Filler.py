from typing import Tuple
from copy import copy

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction

from foundry.core.Address.Address import Address


class Filler:
    """
    A representation of a chunk of data at a location inside a container, wrapping the SQLite backend.
    """

    def __init__(self, filler_id: int):
        self.filler_id = filler_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.filler_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(copy(self.address), self.size)

    @classmethod
    @require_a_transaction
    def from_data(cls, address: Address, size: int, **kwargs):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute("INSERT INTO Fillers (AddressID, Size) VALUES (?, ?)", (address.address_id, size))
        return cls(c.lastrowid)

    @property
    def data(self) -> Tuple[Address, int]:
        return self.address, self.size

    @property
    def inside_container(self) -> bool:
        return self.address.container.size > (self.container_offset + self.size)

    @property
    def space_remaining(self) -> int:
        return self.container.size - self.container_offset - self.size

    @property
    def start_rom_offset(self) -> int:
        return self.address.rom_offset

    @start_rom_offset.setter
    def start_rom_offset(self, rom_offset: int):
        self.address.rom_offset = rom_offset

    @property
    def end_rom_offset(self) -> int:
        return self.start_rom_offset + self.size

    @property
    def start_pc_offset(self) -> int:
        return self.address.pc_offset

    @start_pc_offset.setter
    def start_pc_offset(self, pc_offset: int):
        self.address.pc_offset = pc_offset

    @property
    def end_pc_offset(self) -> int:
        return self.start_pc_offset + self.size

    @property
    def name(self) -> str:
        return self.address.name

    @name.setter
    def name(self, name: str):
        self.address.name = name

    @property
    def container_offset(self) -> int:
        return self.address.container_offset

    @container_offset.setter
    def container_offset(self, container_offset: int):
        self.address.container_offset = container_offset

    @property
    def size(self) -> int:
        with Cursor() as c:
            return c.execute("SELECT Size FROM Fillers WHERE FillerID = ?", (self.filler_id,)).fetchone()[0]

    @size.setter
    @require_a_transaction
    def size(self, size: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute("UPDATE Fillers SET Size = ? WHERE FillerID = ?", (size, self.filler_id))
