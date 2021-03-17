

from dataclasses import dataclass


@dataclass
class Size:
    """
    A 2D representation of a size
    """
    width: int
    height: int

    @classmethod
    def from_size(cls, size: "Size"):
        return cls(size.width, size.height)
