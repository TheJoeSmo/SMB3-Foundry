from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class DrawUpdate(Base):
    __tablename__ = "draw_updates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    filler_id = Column(Integer, ForeignKey("fillers.id"), nullable=False)
    mirror = Column(Boolean, nullable=False)
    top_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)
    bottom_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)

    draw_events = relationship("DrawEvent", backref="draw_updates", cascade="all, delete-orphan")
    top_pattern_table = relationship("PatternTable", remote_side="block_groups.top_pattern_table_id")
    bottom_pattern_table = relationship("PatternTable", remote_side="block_groups.bottom_pattern_table_id")
    filler = relationship("Filler", remote_side="block_groups.filler_id")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name}, {self.rom_offset}, {self.pc_offset}, {self.size})>"

    def __bytes__(self):
        b = bytearray(0x400)
        for (idx, (tl, tr, bl, br)) in enumerate(self.blocks):
            b[idx], b[idx + 0x100], b[idx + 0x200], b[idx + 0x300] = tl, tr, bl, br
        return bytes(b)


class DrawUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DrawUpdate
        include_fk = True
        include_relationships = True
        load_instance = True
