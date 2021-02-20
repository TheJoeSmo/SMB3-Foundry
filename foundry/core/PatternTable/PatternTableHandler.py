

from dataclasses import astuple
from typing import Tuple

from . import CHR_PAGE, graphic_set2chr_index, common_set2chr_index, SPADE_ROULETTE, N_SPADE, VS_2P
from .PatternTable import PatternTable
from foundry.game.File import ROM


def _chr_offset() -> int:
    """
    Get the correct offset into the ROM for the graphics
    """
    return ROM().get_byte(5) * 0x4000 + 0x10


class PatternTableHandler:
    """Makes an artificial PPU for the graphics"""
    def __init__(self, pattern_table: PatternTable):
        self.pattern_table = pattern_table
        self.data = self.get_data(astuple(self.pattern_table))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pattern_table}) with data {self.data}"

    def get_data(self, pattern_table: Tuple[int, int, int, int, int, int]) -> bytearray:
        """Caches the data for quick access"""
        data = bytearray()
        offset = _chr_offset()
        for i in range(2):
            data.extend(ROM().bulk_read(CHR_PAGE * 2, offset + CHR_PAGE * (pattern_table[i] & 0b1111_1110)))
        for i in range(2, 6):
            data.extend(ROM().bulk_read(CHR_PAGE, offset + CHR_PAGE * pattern_table[i]))
        data.extend([0 for _ in range(0x10)])
        return data

    @classmethod
    def from_world_map(cls):
        """Makes a pattern table handler for the world map"""
        return cls(PatternTable(0x14, 0x16, 0x20, 0x21, 0x22, 0x23))

    @classmethod
    def from_tileset(cls, tileset: int):
        """Makes a pattern table handler from a tileset"""
        ptn_tbl = PatternTable(0, 0, 0, 0, 0, 0)

        if tileset not in graphic_set2chr_index and tileset not in common_set2chr_index:
            ptn_tbl.background_0 = tileset
            ptn_tbl.background_1 = tileset
        else:
            ptn_tbl.background_0 = graphic_set2chr_index[tileset]
            ptn_tbl.background_1 = common_set2chr_index[tileset]

            if tileset == SPADE_ROULETTE:
                ptn_tbl.sprite_0 = 0x20
                ptn_tbl.sprite_1 = 0x21
                ptn_tbl.sprite_2 = 0x22
                ptn_tbl.sprite_3 = 0x23
            elif tileset == N_SPADE:
                ptn_tbl.sprite_0 = 0x28
                ptn_tbl.sprite_1 = 0x29
                ptn_tbl.sprite_2 = 0x5A
                ptn_tbl.sprite_3 = 0x31
            elif tileset == VS_2P:
                ptn_tbl.sprite_0 = 0x04
                ptn_tbl.sprite_1 = 0x05
                ptn_tbl.sprite_2 = 0x06
                ptn_tbl.sprite_3 = 0x07
        return cls(ptn_tbl)