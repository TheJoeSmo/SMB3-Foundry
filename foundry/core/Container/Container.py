from typing import Optional, Tuple, List
from copy import deepcopy

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction

from .AbstractContainer import AbstractContainer


class Container(AbstractContainer):
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
        return self.__class__.from_data(self.name, self.rom_offset, self.pc_offset, self.size, self.children)

    def __deepcopy__(self, memo):
        return self.__class__.from_data(
            self.name, self.rom_offset, self.pc_offset, self.size, [deepcopy(child) for child in self.children]
        )

    @classmethod
    @require_a_transaction
    def from_data(
        cls, name: Optional[str], rom_offset: int, pc_offset: int, size: int, children: Optional[List], **kwargs
    ):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO Containers (Name, ROMOffset, PCOffset, Size) VALUES (?, ?, ?, ?)",
            (name, rom_offset, pc_offset, size),
        )
        self = cls(c.lastrowid)
        if children is not None:
            self.children = children
        return self

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

    @property
    def children(self):
        with Cursor() as c:
            return [
                Container(container[0])
                for container in c.execute(
                    "SELECT ChildCID FROM ContainerContainers WHERE ParentCID = ?", (self.container_id,)
                ).fetchall()
            ]

    @children.setter
    @require_a_transaction
    def children(self, children: List, **kwargs):
        self.remove_children()
        for child in children:
            self.add_child(child)

    @require_a_transaction
    def add_child(self, child, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "INSERT INTO ContainerContainers (ParentCID, ChildCID) VALUES (?, ?)",
            (self.container_id, child.container_id),
        )

    @require_a_transaction
    def remove_child(self, child, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "DELETE FROM ContainerContainers WHERE ParentCID = ? AND ChildCID = ?",
            (self.container_id, child.container_id),
        )
