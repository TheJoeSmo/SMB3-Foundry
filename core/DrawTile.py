from sqlalchemy import Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class DrawTile(Base):
    __tablename__ = "draw_tiles"
    draw_event_id = Column(Integer, ForeignKey("draw_events.id"), primary_key=True)
    index = Column(Integer, primary_key=True)
    tile = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name}, {self.rom_offset}, {self.pc_offset}, {self.size})>"


class DrawTileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DrawTile
