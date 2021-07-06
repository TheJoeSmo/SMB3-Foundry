from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


block_group_blocks = Table(
    "block_group_blocks",
    Base.metadata,
    Column("block_group_id", Integer, ForeignKey("block_groups.id"), primary_key=True),
    Column("index", Integer, primary_key=True),
    Column("block_id", Integer, ForeignKey("blocks.id"), nullable=False),
)


block_group_pattern_groups = Table(
    "block_group_pattern_groups",
    Base.metadata,
    Column("block_group_id", Integer, ForeignKey("block_groups.id"), primary_key=True),
    Column("index", Integer, primary_key=True, autoincrement=True),
    Column("pattern_group_id", Integer, ForeignKey("pattern_groups.id"), nullable=False),
)


class BlockGroup(Base):
    __tablename__ = "block_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    name = Column(String)
    offset = Column(Integer, nullable=False)

    pattern_groups = relationship(
        "PatternGroup", secondary=block_group_pattern_groups, collection_class=ordering_list("index"), cascade="all, delete"
    )

    blocks = relationship(
        "Block", secondary=block_group_blocks, collection_class=ordering_list("index"), cascade="all, delete"
    )

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


BlockGroup.__versioned__ = {}
