from typing import List, Tuple, Optional
from copy import copy

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction
from ..Saver.SmartSaver import SmartSaver

from . import get_tsa_offset, get_tsa_pattern_tables, determine_count_of_tilesets
from .ROMTileSquareAssembly import ROMTileSquareAssembly
from .TileSquareAssembly import TileSquareAssembly
from .PatternTable import PatternTable


class ROM(SmartSaver):
    def __init__(self, rom_id: int):
        self.rom_id = rom_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.rom_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {[str(tsa) for tsa in self.tile_square_assemblies]})"

    @require_a_transaction
    def __copy__(self, ignore_name=True, **kwargs):
        cls = self.__class__.from_data(
            None if ignore_name else self.name, [copy(tsa) for tsa in self.tile_square_assemblies]
        )

        # Reorganize the blocks to remove duplicates, as the copy does not handle this functionality.
        TileSquareAssembly.last_blocks = (set(), {})
        for tsa in cls.tile_square_assemblies:
            tsa.from_copy(tsa)

        return cls

    @require_a_transaction
    def from_copy(self, other, ignore_name: bool = True, smart_copy: bool = True, **kwargs):
        if not ignore_name:
            self.name = other.name

        self_tsas, other_tsas = self.tile_square_assemblies, other.tile_square_assemblies

        # Try to not overwrite the tsas, as we can better store information
        if smart_copy and len(self_tsas) == len(other_tsas):
            TileSquareAssembly.last_blocks = (set(), {})
            for tsa in self_tsas:
                for _tsa in other_tsas:
                    if tsa.tsa_offset == _tsa.tsa_offset:
                        tsa.from_copy(_tsa)
                        break
        else:
            self.tile_square_assemblies = [copy(tsa) for tsa in other.tile_square_assemblies]

    @staticmethod
    @require_a_transaction
    def del_temp(**kwargs):
        """
        Removes anything not referenced
        """
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            """
            DELETE ROMs, TileSquareAssemblies, ROMTileSquareAssemblies, TSABlocks, Blocks
            FROM ROMs ROM
            LEFT OUTER JOIN ROMTileSquareAssemblies RTSA ON RTSA.ROMID = ROM.ROMID
            LEFT OUTER JOIN TileSquareAssemblies TSA ON RTSA.TSAID = TSA.TSAID
            LEFT OUTER JOIN TSABlocks TSAB ON TSA.TSAID = TSAB.TSAID
            LEFT OUTER JOIN Blocks ON Blocks.BlockID = TSAB.BlockID
            WHERE ROM.Name = Null
            """
        )

    @classmethod
    @require_a_transaction
    def from_data(cls, name: Optional[str], tile_square_assemblies: List[TileSquareAssembly], **kwargs):
        # todo: is slow

        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO ROMs (Name) VALUES (?)",
            (name,),
        )

        self = cls(c.lastrowid)

        # Self is required beforehand to add its tsas
        for tsa in tile_square_assemblies:
            ROMTileSquareAssembly.from_data(self, tsa)

        return self

    @classmethod
    @require_a_transaction
    def from_rom(cls, name: Optional[str], **kwargs):
        tsas = {(get_tsa_offset(idx), *get_tsa_pattern_tables(idx)) for idx in range(determine_count_of_tilesets())}
        generated_tsas = []

        for (offset, top_ptn_tbl, btm_ptn_tbl) in tsas:
            generated_tsas.append(
                TileSquareAssembly.from_rom(
                    None, offset, PatternTable.from_data(top_ptn_tbl), PatternTable.from_data(btm_ptn_tbl)
                )
            )

        TileSquareAssembly.last_blocks = (set(), {})  # Clean up last blocks used for better block detection

        return cls.from_data(name, generated_tsas)

    @classmethod
    def from_name(cls, name: Optional[str]):
        if cls.rom_exists(name):
            with Cursor() as c:
                return cls(c.execute("SELECT ROMID FROM ROMs WHERE Name = ?", (name,)).fetchone()[0])
        else:
            return cls.from_rom(name)

    @staticmethod
    def rom_exists(name: str) -> bool:
        """
        Determines if a rom exists inside the database that matches the specified values
        """
        if name is None:
            return False  # This is a temporary ROM

        with Cursor() as c:
            c.execute("SELECT EXISTS (SELECT * FROM ROMs WHERE Name = ?)", (name,))
            return bool(c.fetchone()[0])

    @property
    def data(self) -> Tuple[str, List[TileSquareAssembly]]:
        return self.name, self.tile_square_assemblies

    @property
    def name(self):
        with Cursor() as c:
            return c.execute("SELECT Name FROM ROMs WHERE ROMID = ?", (self.rom_id,)).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute("UPDATE ROMs SET Name = ? WHERE ROMID = ?", (name, self.rom_id))

    @property
    def tile_square_assemblies(self) -> List[TileSquareAssembly]:
        with Cursor() as c:
            return [
                ROMTileSquareAssembly(rom_tsa_id[0]).tile_square_assembly
                for rom_tsa_id in c.execute(
                    """
                    SELECT ROMTSAID
                    FROM ROMTileSquareAssemblies
                    WHERE ROMID = ?
                    """,
                    (self.rom_id,),
                ).fetchall()
            ]

    @tile_square_assemblies.setter
    @require_a_transaction
    def tile_square_assemblies(self, tile_square_assemblies: List[TileSquareAssembly], **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "DELETE FROM ROMTileSquareAssemblies WHERE ROMTileSquareAssemblies.ROMID = ?", (self.rom_id,)
        )

        for tile_square_assembly in tile_square_assemblies:
            ROMTileSquareAssembly.from_data(self, tile_square_assembly)

    def apply_to_rom(self):
        for tile_square_assembly in self.tile_square_assemblies:
            tile_square_assembly.apply_to_rom()
