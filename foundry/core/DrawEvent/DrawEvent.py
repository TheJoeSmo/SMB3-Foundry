from typing import List, Tuple
from copy import copy

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction


class DrawEvent:
    """
    A single event to be drawn by the PPU, wrapping the SQLite backend.
    """

    def __init__(self, draw_event_id: int):
        self.draw_event_id = draw_event_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.draw_event_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(
            self.ppu_address, self.is_horizontal, self.repeats, self.tile_count, [copy(tile) for tile in self.tiles]
        )

    @classmethod
    @require_a_transaction
    def from_data(
        cls, ppu_address: int, is_horizontal: bool, repeats: bool, tile_count: int, tiles: List[int], **kwargs
    ):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO DrawEvents (PPUAddress, Type, Repeat, TileCount) VALUES (?, ?, ?, ?)",
            (ppu_address, is_horizontal, repeats, tile_count),
        )

        # We need to create the tiles to do its operations correctly
        self = cls(c.lastrowid)
        self.tiles = tiles

        return self

    @property
    def data(self) -> Tuple[int, bool, bool, int, List]:
        return self.ppu_address, self.is_horizontal, self.repeats, self.tile_count, self.tiles

    @property
    def ppu_address(self) -> int:
        with Cursor() as c:
            return c.execute(
                "SELECT PPUAddress FROM DrawEvents WHERE DrawEventID = ?", (self.draw_event_id,)
            ).fetchone()[0]

    @ppu_address.setter
    @require_a_transaction
    def ppu_address(self, ppu_address: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawEvents SET PPUAddress = ? WHERE DrawEventID = ?", (ppu_address, self.draw_event_id)
        )

    @property
    def is_horizontal(self) -> bool:
        with Cursor() as c:
            return bool(
                c.execute("SELECT Type FROM DrawEvents WHERE DrawEventID = ?", (self.draw_event_id,)).fetchone()[0]
            )

    @is_horizontal.setter
    @require_a_transaction
    def is_horizontal(self, is_horizontal: bool, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawEvents SET Type = ? WHERE DrawEventID = ?", (int(is_horizontal), self.draw_event_id)
        )

    @property
    def is_vertical(self) -> bool:
        return not self.is_horizontal

    @is_vertical.setter
    def is_vertical(self, is_vertical: bool):
        self.is_horizontal = not is_vertical

    @property
    def repeats(self) -> bool:
        with Cursor() as c:
            return bool(
                c.execute("SELECT Repeats FROM DrawEvents WHERE DrawEventID = ?", (self.draw_event_id,)).fetchone()[0]
            )

    @repeats.setter
    @require_a_transaction
    def repeats(self, repeats: bool, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawEvents SET Repeats = ? WHERE DrawEventID = ?", (int(repeats), self.draw_event_id)
        )

    @property
    def tile_count(self) -> int:
        with Cursor() as c:
            return c.execute(
                "SELECT TileCount FROM DrawEvents WHERE DrawEventID = ?", (self.draw_event_id,)
            ).fetchone()[0]

    @tile_count.setter
    @require_a_transaction
    def tile_count(self, tile_count: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawEvents SET TileCount = ? WHERE DrawEventID = ?", (int(tile_count), self.draw_event_id)
        )

    @property
    def tiles(self) -> List[int]:
        from foundry.core.DrawTile.DrawTile import DrawTile

        if self.repeats:
            return [DrawTile(self.draw_event_id, 0).tile] * self.tile_count
        else:
            return [DrawTile(self.draw_event_id, idx).tile for idx in range(self.tile_count)]

    @tiles.setter
    @require_a_transaction
    def tiles(self, tiles: List[int], **kwargs):
        from foundry.core.DrawTile.DrawTile import DrawTile

        assert len(tiles) <= 64  # Will have conflicts otherwise

        transaction = kwargs["transaction"]
        # Delete the current tiles as they will cause problems later otherwise.
        transaction.connection.execute("DELETE FROM DrawTiles WHERE DrawEventID = ?", (self.draw_event_id,))

        self.tile_count = len(tiles)
        for idx, tile in enumerate(tiles):
            DrawTile.from_data(self, idx, tile)

    def to_bytes(self) -> bytes:
        b = bytearray()
        address = self.ppu_address

        b.append((address & 0xFF00) >> 8)
        b.append(address & 0xFF)
        b.append(self.is_horizontal << 7 + self.repeats << 6 + self.tile_count)
        b.extend(self.tiles)

        return bytes(b)
