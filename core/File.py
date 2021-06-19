from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    pattern_tables = relationship("PatternTable", backref="file", cascade="all, delete-orphan")
    block_groups = relationship("BlockGroup", backref="file", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name})>"


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_fk = True
        include_relationships = True
        load_instance = True
