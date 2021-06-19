from sqlalchemy import Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class DrawTile(Base):
    __tablename__ = "draw_tiles"
    __table_args__ = ForeignKeyConstraint(
        ["draw_update_id", "draw_event_index"], ["draw_events.draw_update_id", "draw_events.index"]
    )
    draw_update_id = Column(Integer, ForeignKey("draw_updates"), primary_key=True)
    draw_event_index = Column(Integer, primary_key=True)
    index = Column(Integer, primary_key=True)
    tile = Column(Integer, nullable=False)

    draw_event = relationship("DrawEvent", remote_side=[draw_update_id, draw_event_index])

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name}, {self.rom_offset}, {self.pc_offset}, {self.size})>"


class DrawTileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DrawTile
        include_fk = True
        include_relationships = True
        load_instance = True
