from foundry.core.Cursor.Cursor import Cursor, require_a_transaction
from foundry.core.DrawEvent.DrawEvent import DrawEvent


class DrawUpdateEvent:
    """
    A representation of an event to be drawn by an update, wrapping the SQLite backend.
    """

    def __init__(self, draw_update, index: int):
        self.draw_update_event_id = (
            draw_update.draw_update_id,
            index,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.draw_update_event_id[0]}, {self.draw_update_event_id[1]})"

    def __str__(self) -> str:
        from foundry.core.DrawUpdate.DrawUpdate import DrawUpdate

        return f"{self.__class__.__name__}({DrawUpdate(self.draw_update_event_id[0])}, {self.draw_update_event_id[1]}, {self.event})"

    @classmethod
    @require_a_transaction
    def from_data(cls, draw_update, index: int, draw_event: DrawEvent, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "INSERT INTO DrawTiles (UpdateIndex, DrawUpdateID, DrawEventID) VALUES (?, ?, ?)",
            (index, draw_update.draw_update_id, draw_event.draw_event_id),
        )
        return cls(draw_update.draw_update_id, index)

    @property
    def event(self) -> DrawEvent:
        with Cursor() as c:
            return DrawEvent(
                c.execute(
                    "SELECT DrawEventID FROM DrawUpdateEvents WHERE UpdateIndex = ? AND DrawUpdateID = ?",
                    self.draw_update_event_id,
                ).fetchone()[0]
            )

    @event.setter
    @require_a_transaction
    def block(self, event: DrawEvent, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawUpdateEvents Set DrawEventID = ? WHERE UpdateIndex = ? AND DrawUpdateID = ?",
            (event.draw_event_id, *self.draw_update_event_id),
        )
