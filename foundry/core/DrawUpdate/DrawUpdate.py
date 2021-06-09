from typing import List, Tuple

from foundry.core.Cursor.Cursor import Cursor, require_a_transaction
from foundry.core.Filler.Filler import Filler
from foundry.core.DrawEvent.DrawEvent import DrawEvent
from foundry.core.TileSquareAssembly.PatternTable import PatternTable


class DrawUpdate:
    """
    Multiple events to be written to the PPU, wrapping the SQLite backend.
    """

    def __init__(self, draw_update_id: int):
        self.draw_update_id = draw_update_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.draw_update_id})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def __copy__(self):
        return self.__class__.from_data(self.name, self.filler, self.mirror, self.pattern_tables, self.events)

    @classmethod
    @require_a_transaction
    def from_data(
        cls,
        name: str,
        filler: Filler,
        mirror: bool,
        pattern_tables: Tuple[PatternTable, PatternTable],
        events: List[DrawEvent],
        **kwargs,
    ):
        transaction = kwargs["transaction"]
        c = transaction.cursor
        c.execute(
            "INSERT INTO DrawUpdates (Name, FillerID, Mirror, TopPTID, BottomPTID) VALUES (?, ?, ?, ?, ?)",
            (name, filler.filler_id, mirror, pattern_tables[0].pattern_table_id, pattern_tables[1].pattern_table_id),
        )

        # We need to create the events to do its operations correctly
        self = cls(c.lastrowid)
        self.events = events

        return self

    @property
    def data(self) -> Tuple[str, Filler, bool, Tuple[PatternTable, PatternTable], List[DrawEvent]]:
        return self.name, self.filler, self.mirror, self.pattern_tables, self.events

    @property
    def name(self) -> str:
        with Cursor() as c:
            return c.execute(
                "SELECT PPUAddress FROM DrawUpdates WHERE DrawUpdateID = ?", (self.draw_update_id,)
            ).fetchone()[0]

    @name.setter
    @require_a_transaction
    def name(self, name: str, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawUpdates SET Name = ? WHERE DrawUpdateID = ?", (name, self.draw_update_id)
        )

    @property
    def filler(self) -> Filler:
        with Cursor() as c:
            return Filler(
                c.execute("SELECT FillerID FROM DrawUpdates WHERE DrawUpdateID = ?", (self.draw_update_id,)).fetchone()[
                    0
                ]
            )

    @filler.setter
    @require_a_transaction
    def filler(self, filler: Filler, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawUpdates SET Filler = ? WHERE DrawUpdateID = ?", (filler.filler_id, self.draw_update_id)
        )

    @property
    def mirror(self) -> bool:
        with Cursor() as c:
            return bool(
                c.execute("SELECT Mirror FROM DrawUpdates WHERE DrawUpdateID = ?", (self.draw_update_id,)).fetchone()[0]
            )

    @mirror.setter
    @require_a_transaction
    def mirror(self, mirror: bool, **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawUpdates SET Mirror = ? WHERE DrawUpdateID = ?", (mirror, self.draw_update_id)
        )

    @property
    def pattern_tables(self) -> Tuple[PatternTable, PatternTable]:
        with Cursor() as c:
            ptn_tbl_ids = c.execute(
                "SELECT TopPTID, BottomPTID FROM DrawUpdates WHERE DrawUpdateID = ?", (self.draw_update_id,)
            ).fetchone()[0:2]
            return PatternTable(ptn_tbl_ids[0]), PatternTable(ptn_tbl_ids[1])

    @pattern_tables.setter
    @require_a_transaction
    def pattern_tables(self, pattern_tables: Tuple[PatternTable, PatternTable], **kwargs):
        transaction = kwargs["transaction"]
        transaction.connection.execute(
            "UPDATE DrawUpdates SET TopPTID = ?, BottomPTID = ? WHERE DrawUpdateID = ?",
            (pattern_tables[0].pattern_table_id, pattern_tables[1].pattern_table_id, self.draw_update_id),
        )

    @property
    def events(self) -> List[DrawEvent]:
        with Cursor() as c:
            return [
                DrawEvent(event_id)
                for event_id in c.execute(
                    "SELECT DrawEventID FROM DrawUpdateEvents WHERE DrawUpdateID = ? ORDER BY UpdateIndex",
                    (self.draw_update_id,),
                ).fetchall()
            ]

    @events.setter
    @require_a_transaction
    def events(self, events: List[DrawEvent], **kwargs):
        from foundry.core.DrawUpdateEvent.DrawUpdateEvent import DrawUpdateEvent

        transaction = kwargs["transaction"]
        # Delete the current events as they will cause problems later otherwise.
        transaction.connection.execute("DELETE FROM DrawUpdateEvents WHERE DrawUpdateID = ?", (self.draw_update_id,))

        for idx, event in enumerate(events):
            DrawUpdateEvent.from_data(self, idx, event)

    def to_bytes(self) -> bytes:
        b = bytearray()
        for event in self.events:
            b + event.to_bytes()
        b.append(0x00)  # Denotes the end of the update inside the ROM

        return bytes(b)
