from dataclasses import dataclass


@dataclass
class BlockMeta:
    """A class to describe a block to the BlockHandler"""
    tileset_offset: int
    top_left: int
    top_right: int
    bottom_left: int
    bottom_right: int
