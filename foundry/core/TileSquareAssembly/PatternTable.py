from typing import Tuple

from foundry.core.Cursor.Cursor import Cursor, request_to_be_inside_transaction, require_a_transaction


class PatternTable:
    """
    A representation of a background pattern table consisting of 128 tiles, wrapping the SQLite backend.
    """

    def __init__(self, pattern_table_id: int):
        self.pattern_table_id = pattern_table_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pattern_table_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.offset})"

    def __copy__(self):
        return self.__class__.from_data(self.offset)

    @classmethod
    @require_a_transaction
    def from_data(cls, offset: int, **kwargs):
        """
        Generates a pattern table from utilizing the underlying SQLite fields.
        @param offset: The indexed reference to the pattern table in ROM.
        """
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute("INSERT INTO PatternTables (PTOffset) VALUES (?)", (offset,))
        return cls(c.lastrowid)

    @property
    def data(self) -> Tuple[int]:
        return (self.pattern_table_id,)

    @property
    @request_to_be_inside_transaction
    def offset(self, **kwargs):
        """
        The indexed reference to the pattern table in ROM.
        Each increment results in the true offset in ROM being +/- 128 tiles, 0x500 bytes.

        Note: The offset is used inside some transactions, so it requests to be inside if neccissary.
        """

        def offset(cur):
            return cur.execute(
                "SELECT PTOffset FROM PatternTables WHERE PTID = ?", (self.pattern_table_id,)
            ).fetchone()[0]

        transaction = kwargs["transaction"]

        if transaction is None:
            with Cursor() as c:
                return offset(c)
        else:
            return offset(transaction.cursor)

    @offset.setter
    @require_a_transaction
    def offset(self, offset: int, **kwargs):
        transaction = kwargs["transaction"]
        c = transaction.connection
        c.execute(
            "UPDATE PatternTables SET PTOffset = ? WHERE PTID = ?",
            (
                offset,
                self.pattern_table_id,
            ),
        )
