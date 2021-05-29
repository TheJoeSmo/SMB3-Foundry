from typing import Optional, Tuple, Set, List, Dict
from copy import copy

from foundry.game.File import ROM as File

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction
from foundry.core.Saver.Saver import Saver

from .Block import Block
from .PatternTable import PatternTable


class TileSquareAssembly(Saver):
    """
    A representation of a tile square assembly, wrapping the SQLite backend.
    A tile square assembly is the core proponent of SMB3, being utilized by the respective tilesets.
    Each tile square assembly contains 0x100 blocks, only storing their pattern information.
    The palette information for a given block is determined by its index inside the tile square assembly.
    There are four equal partitions of the tile square assembly, which correspond to the respective palettes.
    """

    last_blocks: Tuple[Set, Dict] = (set(), {})  # Used for efficient generation of TSAs

    def __init__(self, tsa_id: int):
        self.tsa_id = tsa_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tsa_id})"

    def __str__(self) -> str:
        top_ptn_tbl, btm_ptn_tbl = self.pattern_tables
        return (
            f"{self.__class__.__name__}({self.name}, {self.tsa_offset},"
            f"{str(top_ptn_tbl)}, {str(btm_ptn_tbl)}, {[str(block) for block in self.blocks]})"
        )

    @require_a_transaction
    def __copy__(self, **kwargs):
        return self.__class__.from_data(
            self.name,
            self.tsa_offset,
            *[copy(ptn_tbl) for ptn_tbl in self.pattern_tables],
            [copy(block) for block in self.blocks],
        )

    @require_a_transaction
    def from_copy(self, other, known_blocks: Optional[Tuple[Set, Dict]] = None, **kwargs):
        self.name = other.name
        self.tsa_offset = other.tsa_offset
        self.pattern_tables = [copy(ptn_tbl) for ptn_tbl in other.pattern_tables]

        # Respect block patterns.  It also respects names, as the user may have provided custom names
        blocks = []
        blocks_set, blocks_lookup = known_blocks or self.__class__.last_blocks or (set(), {})
        for block in other.blocks:
            if block_meta := (*self.pattern_tables, block.name, *block.patterns) not in blocks_set:
                blocks_set.add(block_meta)
                blocks_lookup.update({block_meta: copy(block)})
            blocks.append(blocks_lookup[block_meta])
        self.blocks = blocks

        self.__class__.last_blocks = (blocks_set, blocks_lookup)  # Update the blocks to represent the new tileset

    @classmethod
    @require_a_transaction
    def from_data(
        cls,
        name: Optional[str],
        tsa_offset: int,
        top_ptn_tbl: PatternTable,
        btm_ptn_tbl: PatternTable,
        blocks: List[Block],
        **kwargs,
    ):
        """
        Generates a tile square assembly from utilizing the underlying SQLite fields.
        @param name: The name of the tile square assembly, used primarily for user convenience.
        @param tsa_offset: The offset in ROM to the tile square assembly block data.
        @param top_ptn_tbl: The pattern table representing the first 0x80 tiles for the blocks.
        @param btm_ptn_tbl: The pattern table representing the last 0x80 tiles for the blocks.
        @param blocks: The list of the 0x100 blocks representing the tile square assembly, to be associated.
        """
        from .TSABlock import create_tsa_blocks_for_tile_square_assembly

        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO TileSquareAssemblies (Name, TSAOffset, TopPTID, BottomPTID) VALUES (?, ?, ?, ?)",
            (
                name,
                tsa_offset,
                top_ptn_tbl.pattern_table_id,
                btm_ptn_tbl.pattern_table_id,
            ),
        )

        # We need to create the tsa to do its operations correctly
        self = cls(c.lastrowid)
        create_tsa_blocks_for_tile_square_assembly(self, blocks)

        return self

    @classmethod
    @require_a_transaction
    def from_rom(
        cls,
        name: Optional[str],
        tsa_offset: int,
        top_ptn_tbl: PatternTable,
        btm_ptn_tbl: PatternTable,
        known_blocks: Optional[Tuple[Set, Dict]] = None,
        **kwargs,
    ):
        """
        Generates a tile square assembly, automatically generating its corresponding blocks.
        @param name: The name of the tile square assembly, used primarily for user convenience.
        @param tsa_offset: The offset in ROM to the tile square assembly block data.
        @param top_ptn_tbl: The pattern table representing the first 0x80 tiles for the blocks.
        @param btm_ptn_tbl: The pattern table representing the last 0x80 tiles for the blocks.
        @param known_blocks: A set and dictionary of blocks to help remove duplicates of blocks throughout the ROM.
        If no known blocks are provided, it will use the class variable last blocks.
        It is recommended that last blocks are cleared prior to calling this routine, to stop anomalies.
        """
        data = File().bulk_read(0x400, tsa_offset)
        blocks = []
        blocks_set, blocks_lookup = known_blocks or cls.last_blocks

        for i in range(0x100):
            tl, tr, bl, br = data[i], data[i + 0x100], data[i + 0x200], data[i + 0x300]
            if (
                block_meta := (
                    top_ptn_tbl.offset,
                    btm_ptn_tbl.offset,
                    tl,
                    tr,
                    bl,
                    br,
                )
                not in blocks_set
            ):
                blocks_set.add(block_meta)
                blocks_lookup.update({block_meta: Block.from_data(None, tl, tr, bl, br)})
            blocks.append(blocks_lookup[block_meta])

        cls.last_blocks = (blocks_set, blocks_lookup)  # Update the blocks to represent the new tileset

        self = cls.from_data(name, tsa_offset, top_ptn_tbl, btm_ptn_tbl, blocks)

        return self

    @property
    def data(self) -> Tuple[str, int, Tuple[PatternTable, PatternTable], List[Block]]:
        """
        The underlying data the tile square assembly is representing.
        @return: A tuple containing the name of the tile square assembly,
        its pattern tables, and its corresponding blocks.
        """
        return self.name, self.tsa_offset, self.pattern_tables, self.blocks

    @property
    def name(self):
        """
        The name of the tile square assembly, used primarily for user convenience.
        """
        with Cursor() as c:
            return c.execute("SELECT Name FROM TileSquareAssemblies WHERE TSAID = ?", (self.tsa_id,)).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute("UPDATE TileSquareAssemblies SET Name = ? WHERE TSAID = ?", (name, self.tsa_id))

    @property
    def tsa_offset(self):
        """
        The offset in ROM to the tile square assembly block data.
        """
        with Cursor() as c:
            return c.execute("SELECT TSAOffset FROM TileSquareAssemblies WHERE TSAID = ?", (self.tsa_id,)).fetchone()[0]

    @tsa_offset.setter
    @require_a_transaction
    def tsa_offset(self, tsa_offset: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE TileSquareAssemblies SET TSAOffset = ? WHERE TSAID = ?", (tsa_offset, self.tsa_id)
        )

    @property
    def pattern_tables(self) -> Tuple[PatternTable, PatternTable]:
        """
        The pattern tables utilized by the tile square assembly to display the correct tiles for its respective blocks.
        """
        with Cursor() as c:
            ptn_tbl_ids = c.execute(
                "SELECT TopPTID, BottomPTID FROM TileSquareAssemblies WHERE TSAID = ?", (self.tsa_id,)
            ).fetchone()[0:2]
            return PatternTable(ptn_tbl_ids[0]), PatternTable(ptn_tbl_ids[1])

    @pattern_tables.setter
    @require_a_transaction
    def pattern_tables(self, pattern_tables: Tuple[PatternTable, PatternTable], **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE TileSquareAssemblies SET TopPTID = ?, BottomPTID = ? WHERE TSAID = ?",
            (pattern_tables[0].pattern_table_id, pattern_tables[1].pattern_table_id, self.tsa_id),
        )

    @property
    def tsa_blocks(self) -> List:
        """
        The list of the underlying connections of the tile square assembly and its blocks.
        Note: These connections cannot be changed directly, due to the fixed nature of the tile square assembly.
        """
        from .TSABlock import TSABlock

        # Since the TSA is a fixed size, there is no reason to ping the database
        return [TSABlock(self.tsa_id, idx) for idx in range(0x100)]

    @tsa_blocks.setter
    @require_a_transaction
    def tsa_blocks(self, blocks: List[Block], **kwargs):
        # You cannot set the tsa blocks, due to the primary key, so this will just work like blocks
        self.blocks = blocks

    @property
    def blocks(self) -> List[Block]:
        """
        The list of the underlying blocks for the tile square assembly.
        """
        return [tsa_block.block for tsa_block in self.tsa_blocks]

    @blocks.setter
    @require_a_transaction
    def blocks(self, blocks: List[Block], **kwargs):
        from .TSABlock import TSABlock

        for idx, block in enumerate(blocks):
            TSABlock(self.tsa_id, idx).block = block

    def to_bytes(self):
        with Cursor() as c:
            blocks = [
                (tl, tr, bl, br)
                for tl, tr, bl, br in c.execute(
                    """
                        SELECT TopLeft, TopRight, BottomLeft, BottomRight
                        FROM TSABlocks
                        LEFT JOIN Blocks ON TSABlocks.BlockID=Blocks.BlockID
                        WHERE TSABlocks.TSAID=?
                        ORDER BY BlockIndex
                        """,
                    (self.tsa_id,),
                )
            ]

        tl, tr, bl, br = [bytearray(patterns[i] for patterns in blocks) for i in range(4)]
        return tl + tr + bl + br

    def apply_to_rom(self):
        """
        Writes the tile square assembly data to the file currently loaded.
        """
        with Cursor() as c:
            blocks = [
                (tl, tr, bl, br)
                for tl, tr, bl, br in c.execute(
                    """
                        SELECT TopLeft, TopRight, BottomLeft, BottomRight
                        FROM TSABlocks
                        LEFT JOIN Blocks ON TSABlocks.BlockID=Blocks.BlockID
                        WHERE TSABlocks.TSAID=?
                        ORDER BY BlockIndex
                        """,
                    (self.tsa_id,),
                )
            ]

        tl, tr, bl, br = [bytearray(patterns[i] for patterns in blocks) for i in range(4)]
        File().bulk_write(tl + tr + bl + br, self.tsa_offset)
