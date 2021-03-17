

from dataclasses import dataclass
from foundry.core.PatternTable import graphic_set2chr_index, common_set2chr_index


@dataclass
class PatternTable:
    """Represents the game's pattern table for the chr data"""
    page_0: int
    page_1: int
    page_2: int
    page_3: int

    def __getitem__(self, item: int) -> int:
        if item == 0:
            return self.page_0
        elif item == 1:
            return self.page_1
        elif item == 2:
            return self.page_2
        elif item == 3:
            return self.page_3
        else:
            raise NotImplementedError

    def __setitem__(self, key: int, value: int):
        if key == 0:
            self.page_0 = value
        elif key == 1:
            self.page_1 = value
        elif key == 2:
            self.page_2 = value
        elif key == 3:
            self.page_3 = value
        else:
            raise NotImplementedError

    @classmethod
    def from_pattern_table(cls, pattern_table: "PatternTable"):
        return cls(pattern_table.page_0, pattern_table.page_1, pattern_table.page_2, pattern_table.page_3)

    @classmethod
    def from_background_pattern_table(cls, page_0, page_2):
        """The background only stores two background pattern tables"""
        return cls(page_0, page_0 + 1, page_2, page_2 + 1)

    @classmethod
    def from_tileset(cls, tileset: int):
        """Makes a pattern table handler from a tileset"""
        if tileset not in graphic_set2chr_index and tileset not in common_set2chr_index:
            return cls.from_background_pattern_table(tileset, tileset)
        else:
            return cls.from_background_pattern_table(graphic_set2chr_index[tileset], common_set2chr_index[tileset])
