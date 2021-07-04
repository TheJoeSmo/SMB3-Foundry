from core.Cursor.Cursor import Cursor, require_a_transaction

from .TileSquareAssembly import TileSquareAssembly


class ROMTileSquareAssembly:
    """
    An intermediate between ROMs and Tilesets to provide a link, wrapping the SQLite backend.
    """

    def __init__(self, rom_tsa_id: int):
        self.rom_tsa_id = rom_tsa_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.rom_tsa_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.rom}, {self.tsa})"

    @classmethod
    @require_a_transaction
    def from_data(cls, rom, tsa: TileSquareAssembly, **kwargs):
        """
        Generates a ROMTileSquareAssembly from utilizing the underlying SQLite fields.
        @param rom: The ROM class correlated with a tile square assembly.
        @param top_left: The tile square assembly associated with the ROM.
        """
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO ROMTileSquareAssemblies (ROMID, TSAID) VALUES (?, ?)",
            (
                rom.rom_id,
                tsa.tsa_id,
            ),
        )

        return cls(c.lastrowid)

    @property
    def tile_square_assembly(self):
        """
        The correlated tile square assembly on this part of the ROM.
        """
        with Cursor() as c:
            return TileSquareAssembly(
                c.execute(
                    "SELECT TSAID FROM ROMTileSquareAssemblies WHERE ROMTSAID = ?", (self.rom_tsa_id,)
                ).fetchone()[0]
            )

    @tile_square_assembly.setter
    @require_a_transaction
    def tile_square_assembly(self, tile_square_assembly: TileSquareAssembly, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE ROMTileSquareAssemblies SET TSAID = ? WHERE ROMTSAID = ?",
            (
                tile_square_assembly.tsa_id,
                self.rom_tsa_id,
            ),
        )
