from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class PatternGroup(Base):
    __tablename__ = "pattern_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    top_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)
    bottom_pattern_table_id = Column(Integer, ForeignKey("pattern_tables.id"), nullable=False)

    top_pattern_table = relationship("PatternTable", foreign_keys=[top_pattern_table_id])
    bottom_pattern_table = relationship("PatternTable", foreign_keys=[bottom_pattern_table_id])

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.file_id}, {self.index})>"


class PatternGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PatternGroup


PatternGroup.__versioned__ = {}
