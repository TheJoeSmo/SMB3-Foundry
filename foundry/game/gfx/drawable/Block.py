

from typing import List, Union
import numpy as np

from foundry.game.File import ROM
from foundry.game.gfx.PatternTableHandler import PatternTableHandler
from foundry.game.gfx.drawable.Tile import Tile, get_color
from foundry.game.gfx.drawable import MASK_COLOR
from PySide2.QtGui import QColor
from foundry.game.gfx.Palette import PaletteSet

TSA_BANK_0 = 0 * 256
TSA_BANK_1 = 1 * 256
TSA_BANK_2 = 2 * 256
TSA_BANK_3 = 3 * 256
TSA_BANKS = [TSA_BANK_0, TSA_BANK_2, TSA_BANK_1, TSA_BANK_3]


def get_block(block_index, palette_group, graphics_set, tsa_data):
    if block_index > 0xFF:
        rom_block_index = ROM().get_byte(block_index)  # block_index is an offset into the graphic memory
        block = Block.from_rom(rom_block_index, palette_group, graphics_set, tsa_data)
    else:
        block = Block.from_rom(block_index, palette_group, graphics_set, tsa_data)

    return block


class Block(Tile):
    image_length = 0x10
    image_height = image_length

    def __init__(self, pixels: bytes, index: int = 0, mask_color: QColor = QColor(*MASK_COLOR).rgb()) -> None:
        super().__init__(pixels=pixels, mask_color=mask_color)
        self.index = index

    @classmethod
    def from_rom(
            cls,
            block_index: int,
            palette_group: Union[PaletteSet, List[List[int]]],
            graphics_page: PatternTableHandler,
            tsa_data: bytes,
            mirrored=False
    ):
        """Returns a block directly from rom"""
        palette_index = (block_index & 0b1100_0000) >> 6
        mask_color = QColor(*get_color(0, palette_group[palette_index])).rgb()
        image = np.empty((Block.image_length, Block.image_length * 3), dtype="ubyte")
        for idx in range(4):
            tile = Tile.from_rom(tsa_data[TSA_BANKS[idx] + block_index], palette_group, palette_index, graphics_page)
            x_off, y_off = (idx % 2) * 3 * Tile.image_length, (idx // 2) * Tile.image_length
            image[y_off:y_off + Tile.image_length, x_off:x_off + 3 * Tile.image_length] = tile.numpy_image
        return cls(bytes(image.flatten().tolist()), block_index, mask_color)
