from typing import Optional, Tuple

from core.Cursor.Cursor import Cursor, require_a_transaction


class Block:
    """
    A representation of a 16x16 pixel block, wrapping the SQLite backend.
    """

    def __init__(self, block_id: int):
        self.block_id = block_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.block_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(self.name, *self.patterns)

    @classmethod
    @require_a_transaction
    def from_data(
        cls, name: Optional[str], top_left: int, top_right: int, bottom_left: int, bottom_right: int, **kwargs
    ):
        """
        Generates a block from utilizing the underlying SQLite fields.
        @param name: The name of the block, used primarly for user convience.
        @param top_left: The top left pattern index of the block.
        @param top_right: The top right pattern index of the block.
        @param bottom_left: The bottom left pattern index of the block.
        @param bottom_right: The bottom right pattern index of the block.
        """
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO BLOCKS (Name, TopLeft, TopRight, BottomLeft, BottomRight) VALUES (?, ?, ?, ?, ?)",
            (name, top_left, top_right, bottom_left, bottom_right),
        )
        last = c.lastrowid

        return cls(last)

    @property
    def data(self) -> Tuple[str, int, int, int, int]:
        """
        The underlying data the block is representing.
        @return: A tuple containing the name of the block and its respective pattern indexes.
        """
        return self.name, *self.patterns

    @property
    def name(self):
        """
        The name of the block, used primarly for user convience.
        """
        with Cursor() as c:
            return c.execute("SELECT Name FROM Blocks WHERE BlockID = ?", (self.block_id,)).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute("UPDATE Blocks SET Name = ? WHERE BlockID = ?", (name, self.block_id))

    @property
    def patterns(self):
        """
        The patterns indexes of the block, represented by the tile square assembly's pattern tables.
        """
        with Cursor() as c:
            return c.execute(
                "SELECT TopLeft, TopRight, BottomLeft, BottomRight FROM Blocks WHERE BlockID = ?", (self.block_id,)
            ).fetchone()

    @patterns.setter
    @require_a_transaction
    def patterns(self, patterns: Tuple[int, int, int, int], **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE Blocks SET TopLeft = ?, TopRight = ?, BottomLeft = ?, BottomRight = ? WHERE BlockID = ?",
            (*patterns, self.block_id),
        )
