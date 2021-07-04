from enum import Enum
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy import Enum as Enum_
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class DrawEventType(Enum):
    horizontal = 1
    verticle = 2


class DrawEvent(Base):
    __tablename__ = "draw_events"
    id = Column(Integer, primary_key=True)
    draw_update_id = Column(Integer, ForeignKey("draw_updates.id"))
    index = Column(Integer)
    address = Column(Integer, nullable=False)
    type = Column(Enum_(DrawEventType), nullable=False)
    repeat = Column(Boolean, nullable=False)

    tiles = relationship("DrawTile", backref="draw_event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.address}, {self.type}, {self.repeat})>"

    def __bytes__(self) -> bytes:
        b = bytearray()
        address = self.address

        b.append((address & 0xFF00) >> 8)
        b.append(address & 0xFF)
        b.append(0x80 if DrawEventType.horizontal is self.type else 0 + self.repeats << 6 + len(self.tiles))
        b.extend([tile.tile for tile in self.tiles])

        return bytes(b)


class DrawEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DrawEvent
        include_fk = True
        include_relationships = True
        load_instance = True
