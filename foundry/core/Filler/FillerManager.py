from typing import List

from foundry.core.Cursor.Cursor import Cursor

from .Filler import Filler
from ..DrawUpdate.DrawUpdate import DrawUpdate


_user_types = [DrawUpdate]


class FillerManager(Filler):
    def __bytes__(self) -> bytes:
        b = bytearray(self.size)  # Fill in 0s by default
        for child in self.children:
            # Do not enforce using the entire space, but not vise versa
            child_bytes = bytes(child)
            b[: len(child_bytes)] = child_bytes

        return bytes(b)

    @property
    def children(self) -> List[DrawUpdate]:
        with Cursor() as c:
            return [
                _user_types[type_id](filler_user_id)
                for (filler_user_id, type_id) in c.execute(
                    "SELECT FillerUserID, FUTID FROM FillerUsers WHERE FillerID = ?", (self.filler_id,)
                )
            ]
