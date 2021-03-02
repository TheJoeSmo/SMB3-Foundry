

from typing import Union
from PySide2.QtGui import QImage, QPainter, Qt, QColor

from foundry.core.PaletteSet.PaletteSet import PaletteSet
from foundry.core.Palette.Palette import Palette
from foundry.core.PatternTable.PatternTableHandler import PatternTableHandler

from foundry.game.gfx.GraphicsSet import GraphicsSet
from foundry.game.gfx.Palette import NESPalette, PaletteGroup
from foundry.game.gfx.drawable import MASK_COLOR, bit_reverse
from smb3parse.objects.object_set import CLOUDY_GRAPHICS_SET

PIXEL_OFFSET = 8  # both bits describing the color of a pixel are in separate 8 byte chunks at the same index

BACKGROUND_COLOR_INDEX = 0


class Tile:
    SIDE_LENGTH = 8  # pixel
    WIDTH = SIDE_LENGTH
    HEIGHT = SIDE_LENGTH

    PIXEL_COUNT = WIDTH * HEIGHT
    SIZE = 2 * PIXEL_COUNT // 8  # 1 pixel is defined by 2 bits

    _tile_cache = {}

    def __init__(
        self,
        object_index: int,
        palette_group: Union[PaletteGroup, PaletteSet],
        palette_index: int,
        graphics_set: Union[GraphicsSet, PatternTableHandler],
        mirrored=False,
    ):
        start = object_index * Tile.SIZE

        self.tile_hash = (object_index, str(palette_group), graphics_set.number)  # hash for caching
        self.cached_tiles = dict()

        self.palette = palette_group[palette_index]
        # self.palette = DEFAULT_PALETTE

        self.data = bytearray()
        self.pixels = bytearray()
        self.mask_pixels = bytearray()

        self.data = graphics_set.data[start : start + Tile.SIZE]

        if graphics_set.number == CLOUDY_GRAPHICS_SET:
            self.background_color_index = 2
        else:
            self.background_color_index = 0

        if mirrored:
            self._mirror()

        for i in range(Tile.PIXEL_COUNT):
            byte_index = i // Tile.HEIGHT
            bit_index = 2 ** (7 - (i % Tile.WIDTH))

            left_bit = right_bit = 0

            if self.data[byte_index] & bit_index:
                left_bit = 1

            if self.data[PIXEL_OFFSET + byte_index] & bit_index:
                right_bit = 1

            color_index = (right_bit << 1) | left_bit

            color = self.palette[color_index]

            # add alpha values
            if color_index == self.background_color_index:
                self.pixels.extend(MASK_COLOR)
            else:
                self.pixels.extend(NESPalette[color])

        assert len(self.pixels) == 3 * Tile.PIXEL_COUNT

    @classmethod
    def from_palette(
        cls,
        object_index: int,
        palette: Palette,
        graphics_set: Union[GraphicsSet, PatternTableHandler],
        mirrored=False,
    ):
        """
        Generates a Tile from a Palette instead of requiring a PaletteSet
        :param object_index: The index for the Tile in the PatternTableHandler
        :param palette: The set of colors used for the Tile
        :param graphics_set: The PatternTableHandler used to find the tile in ROM
        :param mirrored: If the tile is flipped vertically
        :return: A Tile
        """
        return cls(
            object_index,
            PaletteSet(palette, palette, palette, palette),
            0,
            graphics_set,
            mirrored
        )

    def as_image(self, tile_length=8):
        if tile_length not in self.cached_tiles.keys():
            width = height = tile_length

            image = QImage(self.pixels, self.WIDTH, self.HEIGHT, QImage.Format_RGB888)

            image = image.scaled(width, height)

            self.cached_tiles[tile_length] = image

        return self.cached_tiles[tile_length]

    def _mirror(self):
        for byte in range(len(self.data)):
            self.data[byte] = bit_reverse[self.data[byte]]

    def draw(self, painter: QPainter, x, y, length):
        tile_hash = (self.tile_hash, length)

        if tile_hash not in Tile._tile_cache:
            Tile._tile_cache[tile_hash] = self.as_image(length)

        painter.drawImage(x, y, Tile._tile_cache[tile_hash])
