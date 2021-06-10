from typing import List

from foundry.core.Cursor.Cursor import Cursor

from .AbstractContainerManager import AbstractContainerManager
from .Container import Container
from ..Filler.Filler import Filler


class ContainerManager(Container, AbstractContainerManager):
    @staticmethod
    def filler_safe_to_save(filler: Filler) -> bool:
        return filler.inside_container

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
