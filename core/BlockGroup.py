from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


block_group_blocks = Table(
    "block_group_blocks",
    Base,
    Column("block_group_id", Integer, ForeignKey("block_groups.id"), primary_key=True),
    Column("index", Integer, primary_key=True),
    Column("block_id", Integer, ForeignKey("blocks.id"), nullable=False),
)


class BlockGroup(Base):
    __tablename__ = "block_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    name = Column(String)
    offset = Column(Integer, nullable=False)
    top_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)
    bottom_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)

    blocks = relationship(
        "Blocks", secondary=block_group_blocks, collection_class=ordering_list("index"), cascade="all, delete"
    )
    top_pattern_table = relationship("PatternTable", remote_side="block_groups.top_pattern_table_id")
    bottom_pattern_table = relationship("PatternTable", remote_side="block_groups.bottom_pattern_table_id")
    file = relationship("File", remote_side="block_groups.file_id")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.file_id}, {self.name}, {self.offset}, {self.top_pattern_table_id}, {self.bottom_pattern_table_id})>"

    def __bytes__(self):
        b = bytearray(0x400)
        for (idx, (tl, tr, bl, br)) in enumerate(self.blocks):
            b[idx], b[idx + 0x100], b[idx + 0x200], b[idx + 0x300] = tl, tr, bl, br
        return bytes(b)


class BlockGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlockGroup
        include_fk = True
        include_relationships = True
        load_instance = True
