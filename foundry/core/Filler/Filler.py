from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from foundry.core import Base


class Filler(Base):
    __tablename__ = "fillers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    size = Column(Integer, nullable=False)

    # different types of valid filler types (select one)
    draw_update_id = Column(Integer, ForeignKey("draw_update.id"))

    # relationships
    address = relationship("Address", remote_side="fillers.address_id")
    draw_update = relationship("DrawUpdate", remote_side="fillers.draw_update_id", cascade="all, delete-orphan")

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
        include_fk = True
        include_relationships = True
        load_instance = True
