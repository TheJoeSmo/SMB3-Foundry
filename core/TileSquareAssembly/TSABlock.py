from typing import Tuple, List
from core.Cursor import Cursor, require_a_transaction

from .Block import Block


@require_a_transaction
def create_tsa_blocks_for_tile_square_assembly(tsa, blocks: List[Block], **kwargs):
    """
    An optimized way to create the tsa blocks.  It starts a transaction, which is much faster in SQLite.
    """
    transaction = kwargs["transaction"]

    values = [
        (
            index,
            tsa.tsa_id,
            block.block_id,
        )
        for index, block in enumerate(blocks)
    ]

    transaction.connection.executemany(
        "INSERT INTO TSABlocks (BlockIndex, TSAID, BlockID) VALUES (?, ?, ?)",
        values,
    )


class TSABlock:
    """
    An intermediate between Blocks and Tilesets to provide a link, wrapping the SQLite backend.
    """

    def __init__(self, tsa_id: int, index: int):
        self.tsa_block_id = (
            tsa_id,
            index,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tsa_block_id[0]}, {self.tsa_block_id[1]})"

    def __str__(self) -> str:
        from .TileSquareAssembly import TileSquareAssembly

        return (
            f"{self.__class__.__name__}({TileSquareAssembly(self.tsa_block_id[0])},"
            f"{self.tsa_block_id[1]}, {str(self.block)})"
        )

    @classmethod
    @require_a_transaction
    def from_data(cls, tsa, index: int, block: Block, **kwargs):
        """
        Generates a tile square assembly block from utilizing the underlying SQLite fields.
        @param tsa: The tile square assembly the block is associated with.
        @param index: The index into the tile square assembly that the block is defined.
        @param block: The block represented.
        """
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO TSABlocks (BlockIndex, TSAID, BlockID) VALUES (?, ?, ?)", (index, tsa.tsa_id, block.block_id)
        )
        return cls(c.lastrowid, index)

    @property
    def block(self) -> Block:
        """
        The correlated block on this part of the tile square assembly.
        """
        with Cursor() as c:
            return Block(
                c.execute(
                    "SELECT BlockID FROM TSABlocks WHERE TSAID = ? AND BlockIndex = ?", self.tsa_block_id
                ).fetchone()[0]
            )

    @block.setter
    @require_a_transaction
    def block(self, block: Block, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE TSABlocks Set BlockID = ? WHERE TSAID = ? AND BlockIndex = ?", (block.block_id, *self.tsa_block_id)
        )

    @property
    def name(self):
        """
        The name of the block, used primarly for user convience.
        """
        return self.block.name

    @name.setter
    def name(self, name: str):
        self.block.name = name

    @property
    def block_patterns(self):
        """
        The patterns indexes of the block, represented by the tile square assembly's pattern tables.
        """
        return self.block.block_patterns

    @block_patterns.setter
    def block_patterns(self, patterns: Tuple[int, int, int, int]):
        self.block.block_patterns = patterns

    @property
    def palette_index(self) -> int:
        """
        The palette index of the block.  This is determined by the index inside the tile square assembly.
        """
        return self.tsa_block_id[1] // 0x40
