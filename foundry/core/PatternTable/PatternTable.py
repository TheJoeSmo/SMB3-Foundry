from dataclasses import dataclass


@dataclass
class PatternTable:
    """Represents the game's pattern table for the chr data"""
    background_0: int
    background_1: int
    sprite_0: int
    sprite_1: int
    sprite_2: int
    sprite_3: int


