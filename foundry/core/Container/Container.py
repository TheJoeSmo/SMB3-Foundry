from typing import Optional, Tuple

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction


class Container:
    """
    A representation of a segment of data, wrapping the SQLite backend.
    """

    def __init__(self, container_id: int):
        self.container_id = container_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.container_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(self.name, self.rom_offset, self.pc_offset, self.size)

    @classmethod
    @require_a_transaction
    def from_data(cls, name: Optional[str], rom_offset: int, pc_offset: int, size: int, **kwargs):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO Containers (Name, ROMOffset, PCOffset, Size) VALUES (?, ?, ?, ?)",
            (name, rom_offset, pc_offset, size),
        )
        return cls(c.lastrowid)

    @property
    def data(self) -> Tuple[str, int, int, int]:
        return self.name, self.rom_offset, self.pc_offset, self.size

    @property
    def name(self) -> str:
        with Cursor() as c:
            return c.execute("SELECT Name FROM Containers WHERE ContainersID = ?", (self.container_id,)).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Containers SET Name = ? WHERE ContainersID = ?", (name, self.container_id)
        )

    @property
    def rom_offset(self) -> int:
        with Cursor() as c:
            return c.execute(
                "SELECT ROMOffset FROM Containers WHERE ContainersID = ?", (self.container_id,)
            ).fetchone()[0]

    @rom_offset.setter
    @require_a_transaction
    def rom_offset(self, rom_offset: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Containers SET ROMOffset = ? WHERE ContainersID = ?", (rom_offset, self.container_id)
        )

    @property
    def pc_offset(self) -> int:
        with Cursor() as c:
            return c.execute("SELECT PCOffset FROM Containers WHERE ContainersID = ?", (self.container_id,)).fetchone()[
                0
            ]

    @pc_offset.setter
    @require_a_transaction
    def pc_offset(self, pc_offset: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Containers SET PCOffset = ? WHERE ContainersID = ?", (pc_offset, self.container_id)
        )

    @property
    def size(self) -> int:
        with Cursor() as c:
            return c.execute("SELECT Size FROM Containers WHERE ContainersID = ?", (self.container_id,)).fetchone()[0]

    @size.setter
    @require_a_transaction
    def size(self, size: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Containers SET Size = ? WHERE ContainersID = ?", (size, self.container_id)
        )
