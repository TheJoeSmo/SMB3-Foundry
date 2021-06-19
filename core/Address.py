from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    offset = Column(Integer, nullable=False)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=False)
    container = relationship("Container", remote_side="addresses.container_id")
    fillers = relationship("Filler", backref="addresses", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.name}, {self.offset}, {self.container_id})>"


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        include_fk = True
        include_relationships = True
        load_instance = True
