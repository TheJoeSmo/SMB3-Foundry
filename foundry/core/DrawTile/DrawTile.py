from foundry.core.Cursor.Cursor import Cursor, require_a_transaction


class DrawTile:
    """
    A representation of tile to be drawn by an event, wrapping the SQLite backend.
    """

    def __init__(self, draw_event, index: int):
        self.draw_tile_id = (
            draw_event.draw_event_id,
            index,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.draw_tile_id[0]}, {self.draw_tile_id[1]})"

    def __str__(self) -> str:
        from foundry.core.DrawEvent.DrawEvent import DrawEvent

        return f"{self.__class__.__name__}({DrawEvent(self.draw_tile_id[0])}, {self.draw_tile_id[1]}, {self.tile})"

    @classmethod
    @require_a_transaction
    def from_data(cls, draw_event, index: int, tile: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "INSERT INTO DrawTiles (EventIndex, DrawEventID, Tile) VALUES (?, ?, ?)",
            (index, draw_event.draw_event_id, tile),
        )
        return cls(draw_event.draw_event_id, index)

    @property
    def tile(self) -> int:
        with Cursor() as c:
            return c.execute(
                "SELECT Tile FROM DrawTiles WHERE EventIndex = ? AND DrawEventID = ?", self.draw_tile_id
            ).fetchone()[0]

    @tile.setter
    @require_a_transaction
    def block(self, tile: int, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawTiles Set Tile = ? WHERE EventIndex = ? AND DrawEventID = ?", (tile, *self.draw_tile_id)
        )
