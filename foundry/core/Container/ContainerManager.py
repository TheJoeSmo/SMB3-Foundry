from typing import List

from foundry.core.Cursor.Cursor import Cursor

from .Container import Container
from ..Filler.Filler import Filler


class ContainerManager(Container):
    def __bytes__(self) -> bytes:
        if not self.safe_to_save:

            def filler_can_save(filler: Filler) -> bool:
                return filler.inside_container

            raise IndexError(
                f"{list(filter(filler_can_save, self.fillers))} cannot be saved to bytes because they are not inside {self}"
            )

        b = bytearray(self.size)  # Fill in 0s by default
        for filler in self.fillers:
            b[filler.container_offset : filler.container_offset + filler.size] = bytes(filler)

        return bytes(b)

    @property
    def safe_to_save(self) -> bool:
        return all([filler.inside_container for filler in self.fillers])

    @property
    def fillers(self) -> List[Filler]:
        with Cursor() as c:
            return [
                Filler(filler[0])
                for filler in c.execute(
                    """
                    SELECT FillerID FROM Fillers 
                    LEFT OUTER JOIN Addreses ON Fillers.AddressID = Addresses.AddressID
                    WHERE ContainerID = ?
                    """,
                    (self.container_id,),
                )
            ]
