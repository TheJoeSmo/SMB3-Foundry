from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core import Base


class Filler(Base):
    __tablename__ = "fillers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    size = Column(Integer, nullable=False)

    # relationships
    draw_update = relationship("DrawUpdate", backref="filler", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.__class__.__tablename__}({self.address_id}, {self.size})>"

    def __bytes__(self) -> bytes:
        b = bytearray(self.size)  # Fill in 0s by default
        for child in self.children:
            # Do not enforce using the entire space, but not vise versa
            child_bytes = bytes(child)
            b[: len(child_bytes)] = child_bytes

        return bytes(b)

    @hybrid_property
    def filler_type(self):
        return self.draw_update_id

    @hybrid_property
    def inside_container(self) -> bool:
        return self.address.container.size > (self.address.offset + self.size)

    @hybrid_property
    def space_remaining(self) -> int:
        return self.address.container.size - self.address.offset - self.size


class FillerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Filler


Filler.__versioned__ = {}