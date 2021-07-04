from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class Container(Base):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    rom_offset = Column(Integer, nullable=False)
    pc_offset = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("containers.id"))

    parent = relationship(
        "Container", backref=backref("children", remote_side=[id]), cascade="all, delete-orphan"
    )
    addresses = relationship("Address", backref="container", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name}, {self.rom_offset}, {self.pc_offset}, {self.size})>"


class ContainerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Container
