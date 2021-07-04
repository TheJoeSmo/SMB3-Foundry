from sqlalchemy import Column, Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class Block(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    top_left = Column(Integer, nullable=False)
    top_right = Column(Integer, nullable=False)
    bottom_left = Column(Integer, nullable=False)
    bottom_right = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.top_left}, {self.top_right}, {self.bottom_left}, {self.bottom_right})>"


class BlockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Block
