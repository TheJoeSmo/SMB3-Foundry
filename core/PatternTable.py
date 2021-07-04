from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class PatternTable(Base):
    __tablename__ = "pattern_tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    index = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.file_id}, {self.index})>"


class PatternTableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PatternTable
        include_fk = True
        include_relationships = True
        load_instance = True
