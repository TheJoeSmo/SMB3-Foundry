from typing import Optional, Tuple
from copy import deepcopy

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction

from .AbstractAddress import AbstractAddress
from ..Container.Container import Container


class Address(AbstractAddress):
    """
    A representation of an index inside a container, wrapping the SQLite backend.
    """

    def __init__(self, address_id: int):
        self.address_id = address_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.address_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(self.name, self.container, self.container_offset)

    def __deepcopy__(self):
        return self.__class__.from_data(self.name, deepcopy(self.container), self.container_offset)

    @classmethod
    @require_a_transaction
    def from_data(cls, name: Optional[str], container: Container, container_offset, **kwargs):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO Addresses (Name, ContainerID, ContainerOffset) VALUES (?, ?, ?)",
            (name, container, container_offset),
        )
        return cls(c.lastrowid)

    @property
    def data(self) -> Tuple[str, Container, int]:
        return self.name, self.container, self.container_offset

    @property
    def name(self) -> str:
        with Cursor() as c:
            return c.execute("SELECT Name FROM Addresses WHERE AddressesID = ?", (self.address_id,)).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute("UPDATE Addresses SET Name = ? WHERE AddressesID = ?", (name, self.address_id))

    @property
    def container(self) -> Container:
        with Cursor() as c:
            return Container(
                c.execute("SELECT ContainerID FROM Addresses WHERE AddressesID = ?", (self.address_id,)).fetchone()[0]
            )

    @container.setter
    @require_a_transaction
    def container(self, container: Container, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Addresses SET ContainerID = ? WHERE AddressesID = ?", (container.container_id, self.address_id)
        )

    @property
    def container_offset(self) -> int:
        with Cursor() as c:
            return c.execute(
                "SELECT ContainerOffset FROM Addresses WHERE AddressesID = ?", (self.address_id,)
            ).fetchone()[0]

    @container_offset.setter
    @require_a_transaction
    def container_offset(self, container_offset: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Addresses SET ContainerOffset = ? WHERE AddressesID = ?", (container_offset, self.address_id)
        )
