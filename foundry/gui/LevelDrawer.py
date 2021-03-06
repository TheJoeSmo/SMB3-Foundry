
import numpy
from typing import Dict
from PySide2.QtCore import QPoint, QRect
from PySide2.QtGui import QBrush, QColor, QImage, QPainter, QPen, Qt

from foundry.core.util.add_selection_graphic_to_image import add_selection_graphic_to_image
from foundry.core.Settings.util import _main_container
from foundry.core.Settings.SmartSettingContainer import SmartSettingContainer
from foundry import data_dir
from foundry.game.File import ROM
from foundry.game.gfx.Palette import load_palette
from foundry.game.gfx.PatternTableHandler import PatternTableHandler
from foundry.game.gfx.drawable.Block import Block
from foundry.game.gfx.objects.EnemyItem import EnemyObject, MASK_COLOR
from foundry.game.gfx.objects.LevelObjectController import LevelObjectController
from foundry.game.gfx.objects.LevelObject import GROUND, SCREEN_HEIGHT, SCREEN_WIDTH
from foundry.game.gfx.objects.ObjectLike import EXPANDS_BOTH, EXPANDS_HORIZ, EXPANDS_VERT
from foundry.game.level.Level import Level
from foundry.gui.AutoScrollDrawer import AutoScrollDrawer
from smb3parse.constants import OBJ_AUTOSCROLL
from foundry.game.Rect import Rect
from foundry.game.Tileset import Tileset
from foundry.gui.QImage.Image import Image

_level_drawer_container = SmartSettingContainer.from_json_file("level_drawer", force=True)
_main_container.set_setting_container("level_drawer", _level_drawer_container)

FIRE_FLOWER = Image.as_custom("fire_flower")
LEAF = Image.as_custom("leaf")
NORMAL_STAR = Image.as_custom("star")
CONTINUOUS_STAR = Image.as_custom("hidden_star")
MULTI_COIN = Image.as_custom("multi_coin")
ONE_UP = Image.as_custom("one_up")
COIN = Image.as_custom("coin")
VINE = Image.as_custom("vine")
P_SWITCH = Image.as_custom("pswitch")
SILVER_COIN = Image.as_custom("silver_coin")
INVISIBLE_COIN = Image.as_custom("hidden_coin")
INVISIBLE_1_UP = Image.as_custom("hidden_one_up")

NO_JUMP = Image.as_custom("warp_disabled")
UP_ARROW = Image.as_custom("up_arrow")
DOWN_ARROW = Image.as_custom("down_arrow")
LEFT_ARROW = Image.as_custom("left_arrow")
RIGHT_ARROW = Image.as_custom("right_arrow")

ITEM_ARROW = Image.as_custom("item_arrow")

EMPTY_IMAGE = Image.as_custom("empty_image")

SPECIAL_BACKGROUND_OBJECTS = [
    "blue background",
    "starry background",
    "underground background under this",
    "sets background to actual background color",
]


def _block_from_index(block_index: int, level: Level) -> Block:
    """
    Returns the block at the given index, from the TSA table for the given level.

    :param block_index:
    :param level:
    :return:
    """

    palette_group = load_palette(level.object_set_number, level.header.object_palette_index)
    graphics_set = PatternTableHandler(level.header.graphic_set_index)
    tsa_data = ROM().get_tsa_data(level.object_set_number)

    return Block.from_rom(block_index, palette_group, graphics_set, tsa_data)


class LevelDrawer:
    def __init__(self):
        self.tsa_data = None

        self.block_length = Block.default_size

        self.grid_pen = QPen(QColor(0x80, 0x80, 0x80, 0x80), width=1)
        self.screen_pen = QPen(QColor(0xFF, 0x00, 0x00, 0xFF), width=1)

        self.request_render_level_blocks = True
        self.last_level_blocks = []
        self.block_from_rom = {}

    def draw(self, painter: QPainter, level: Level, force=False):
        """The draw routine for LevelDrawer"""
        transparency: bool = _level_drawer_container.safe_get_setting("block_transparency", True)

        def draw_objects():
            """Draws the objects of the level"""
            level_rect: Rect = level.get_rect()
            width, height = level_rect.abs_size.width, level_rect.abs_size.height
            real_width, real_height = self.block_length * width, self.block_length * height
            level_blocks = numpy.empty((width, height), dtype="ubyte")

            def level_init():
                """"Initializes the numpy level array"""
                #  todo: Remove function to return premade background from plugin

                def fill_background():
                    """Fills the entire background with a block"""
                    level_blocks.fill(Tileset(level.object_set_number).background_block)

                def fill_sky_background():
                    """Fills the entire background and sets the top to a different block"""
                    fill_background()
                    sky_top = numpy.full(width, 0x86, dtype="ubyte")
                    level_blocks[:, 0] = sky_top

                def fill_desert_background():
                    """Fills the entire background and sets the bottom to the desert ground"""
                    fill_background()
                    ground = numpy.full(width, 0x56, dtype="ubyte")
                    level_blocks[:, -1] = ground

                def fill_fortress_background():
                    """Fills the entire background and sets the bottom floor for the fortress"""
                    fill_background()
                    ground = numpy.empty((width), dtype="ubyte")
                    ground[::2] = 0x14
                    ground[1::2] = 0x15
                    level_blocks[:, -2] = ground
                    ground = numpy.empty((width), dtype="ubyte")
                    ground[::2] = 0x16
                    ground[1::2] = 0x17
                    level_blocks[:, -1] = ground

                background_routine_by_objectset = {
                    0: fill_background,
                    1: fill_background,
                    2: fill_fortress_background,
                    3: fill_background,
                    4: fill_sky_background,
                    5: fill_background,
                    6: fill_background,
                    7: fill_background,
                    8: fill_background,
                    9: fill_desert_background,
                    10: fill_background,
                    11: fill_background,
                    12: fill_sky_background,
                    13: fill_background,
                    14: fill_background,
                    15: fill_background
                }

                background_routine_by_objectset[level.object_set_number]()

            level_init()

            def get_objects():
                """Generates the blocks from the generators"""
                for level_object in level.get_all_objects():

                    if not isinstance(level_object, LevelObjectController):
                        continue
                    for (block, pos) in level_object.get_blocks_and_positions():
                        if block == -1:
                            continue
                        try:
                            level_blocks[pos.x, pos.y] = block
                        except IndexError:
                            pass

            get_objects()

            def get_blocks():
                #  todo: Convert if statement to an observable that gets updated automatically
                """
                if self.block_quick_object_set != level.object_set_number or self.block_length != \
                    self.block_quick_block_length or self.block_transparency != _level_drawer_container.safe_get_setting(
                    "block_transparency", True) \
                        or force:
                """

                if self.request_render_level_blocks or force:
                    palette_set = load_palette(level.object_set_number, level.header.object_palette_index)
                    tsa_data = ROM().get_tsa_data(level.object_set_number)
                    pattern_table = PatternTableHandler.from_tileset(level.header.graphic_set_index)

                    blocks = {}
                    for i in range(0xFF):
                        blocks.update(
                            {
                                i: Block.from_rom(i, palette_set, pattern_table, tsa_data).qpixmap_custom(
                                    self.block_length,
                                    self.block_length,
                                    transparent=transparency
                                )
                            }
                        )
                    self.last_level_blocks = blocks

                return self.last_level_blocks

            def render_blocks(blocks: Dict):
                current_block = 0
                brushes = [QBrush(block) for block in blocks.values()]
                painter.setPen(Qt.NoPen)

                for ix, iy in numpy.ndindex(level_blocks.shape):
                    block = level_blocks[ix, iy]
                    if current_block != block:
                        current_block = block

                        painter.setBrush(brushes[current_block])
                    painter.drawRect(ix * self.block_length, iy * self.block_length, self.block_length, self.block_length)
                painter.setBrush(Qt.NoBrush)

            render_blocks(get_blocks())

            for level_object in level.get_all_objects():
                if level_object.selected:
                    painter.save()

                    painter.setPen(QPen(QColor(0x00, 0x00, 0x00, 0x80), width=1))
                    painter.drawRect(level_object.get_rect(self.block_length))

                    painter.restore()
                if isinstance(level_object, LevelObjectController):
                    continue
                level_object.render()
                level_object.draw(painter, self.block_length, transparency)

        draw_objects()

        self._draw_overlays(painter, level)

        if _level_drawer_container.safe_get_setting("draw_expansion", True):
            self._draw_expansions(painter, level)

        if _level_drawer_container.safe_get_setting("draw_mario", True):
            self._draw_mario(painter, level)

        if _level_drawer_container.safe_get_setting("draw_jumps", True):
            self._draw_jumps(painter, level)

        if _level_drawer_container.safe_get_setting("draw_grid", False):
            self._draw_grid(painter, level)

        if _level_drawer_container.safe_get_setting("draw_auto_scroll", True):
            self._draw_auto_scroll(painter, level)

    def _draw_overlays(self, painter: QPainter, level: Level):
        painter.save()

        for level_object in level.get_all_objects():
            name = level_object.description.lower()

            # only handle this specific enemy item for now
            if isinstance(level_object, EnemyObject) and "invisible door" not in name:
                continue

            pos = level_object.get_rect(self.block_length).topLeft()
            rect = level_object.get_rect(self.block_length)

            # invisible coins, for example, expand and need to have multiple overlays drawn onto them
            # set true by default, since for most overlays it doesn't matter
            fill_object = True

            # pipe entries
            if "pipe" in name and "can go" in name:
                if not _level_drawer_container.safe_get_setting("draw_jump_on_objects", True):
                    continue

                fill_object = False

                # center() is one pixel off for some reason
                pos = rect.topLeft() + QPoint(*(rect.size() / 2).toTuple())

                if "left" in name:
                    image = LEFT_ARROW

                    pos.setX(rect.right())
                    pos.setY(pos.y() - self.block_length / 2)

                elif "right" in name:
                    image = RIGHT_ARROW
                    pos.setX(rect.left() - self.block_length)
                    pos.setY(pos.y() - self.block_length / 2)

                elif "down" in name:
                    image = DOWN_ARROW
                    pos.setX(pos.x() - self.block_length / 2)
                    pos.setY(rect.top() - self.block_length)
                else:
                    image = UP_ARROW
                    pos.setX(pos.x() - self.block_length / 2)
                    pos.setY(rect.bottom())

            elif "door" == name or "door (can go" in name or "invisible door" in name:
                fill_object = False

                if "note" in name:
                    image = UP_ARROW
                else:
                    # door
                    image = DOWN_ARROW

                pos.setY(rect.top() - self.block_length)

            # "?" - blocks, note blocks, wooden blocks and bricks
            elif "'?' with" in name or "brick with" in name or "bricks with" in name or "block with" in name:
                if not _level_drawer_container.safe_get_setting("draw_items_in_blocks", True):
                    continue

                pos.setY(pos.y() - self.block_length)

                if "flower" in name:
                    image = FIRE_FLOWER
                elif "leaf" in name:
                    image = LEAF
                elif "continuous star" in name:
                    image = CONTINUOUS_STAR
                elif "star" in name:
                    image = NORMAL_STAR
                elif "multi-coin" in name:
                    image = MULTI_COIN
                elif "coin" in name:
                    image = COIN
                elif "1-up" in name:
                    image = ONE_UP
                elif "vine" in name:
                    image = VINE
                elif "p-switch" in name:
                    image = P_SWITCH
                else:
                    image = EMPTY_IMAGE

                # draw little arrow for the offset item overlay
                arrow_pos = QPoint(pos)
                arrow_pos.setY(arrow_pos.y() + self.block_length / 4)
                painter.drawImage(arrow_pos, ITEM_ARROW.scaled(self.block_length, self.block_length))

            elif "invisible" in name:
                if not _level_drawer_container.safe_get_setting("draw_invisible_items", True):
                    continue

                if "coin" in name:
                    image = INVISIBLE_COIN
                elif "1-up" in name:
                    image = INVISIBLE_1_UP
                else:
                    image = EMPTY_IMAGE

            elif "silver coins" in name:
                if not _level_drawer_container.safe_get_setting("draw_invisible_items", True):
                    continue

                image = SILVER_COIN
            else:
                continue

            if fill_object:
                for x in range(level_object.rendered_width):
                    adapted_pos = QPoint(pos)
                    adapted_pos.setX(pos.x() + x * self.block_length)

                    image = image.scaled(self.block_length, self.block_length)
                    painter.drawImage(adapted_pos, image)

                    if level_object.selected:
                        painter.drawImage(adapted_pos, add_selection_graphic_to_image(image))

            else:
                image = image.scaled(self.block_length, self.block_length)
                painter.drawImage(pos, image)

        painter.restore()

    @staticmethod
    def _object_in_jump_area(level: Level, level_object: LevelObjectController):
        for jump in level.jumps:
            screen = jump.screen_index

            if level.is_vertical:
                rect = QRect(0, SCREEN_WIDTH * screen, SCREEN_WIDTH, SCREEN_HEIGHT, )
            else:
                rect = QRect(SCREEN_WIDTH * screen, 0, SCREEN_WIDTH, GROUND, )
            try:
                if rect.contains(QPoint(*level_object.get_position())):
                    return True
            except AttributeError:
                return False
        else:
            return False

    def _draw_expansions(self, painter: QPainter, level: Level):
        for level_object in level.get_all_objects():
            if level_object.selected:
                painter.drawRect(level_object.get_rect(self.block_length))

            if _level_drawer_container.safe_get_setting("draw_expansion", True):
                painter.save()

                painter.setPen(Qt.NoPen)

                if level_object.expands() == EXPANDS_BOTH:
                    painter.setBrush(QColor(0xFF, 0, 0xFF, 0x80))
                elif level_object.expands() == EXPANDS_HORIZ:
                    painter.setBrush(QColor(0xFF, 0, 0, 0x80))
                elif level_object.expands() == EXPANDS_VERT:
                    painter.setBrush(QColor(0, 0, 0xFF, 0x80))

                painter.drawRect(level_object.get_rect(self.block_length))

                painter.restore()

    def _draw_mario(self, painter: QPainter, level: Level):
        mario_actions = QImage(str(data_dir / "mario.png"))

        mario_actions.convertTo(QImage.Format_RGBA8888)

        mario_position = QPoint(*level.header.mario_position()) * self.block_length

        x_offset = 32 * level.start_action

        mario_cutout = mario_actions.copy(QRect(x_offset, 0, 32, 32)).scaled(
            2 * self.block_length, 2 * self.block_length
        )

        painter.drawImage(mario_position, mario_cutout)

    def _draw_jumps(self, painter: QPainter, level: Level):
        for jump in level.jumps:
            painter.setBrush(QBrush(QColor(0xFF, 0x00, 0x00), Qt.FDiagPattern))

            painter.drawRect(jump.get_rect(self.block_length, level.is_vertical))

    def _draw_grid(self, painter: QPainter, level: Level):
        panel_width, panel_height = level.get_rect(self.block_length).size().toTuple()

        painter.setPen(self.grid_pen)

        for x in range(0, panel_width, self.block_length):
            painter.drawLine(x, 0, x, panel_height)
        for y in range(0, panel_height, self.block_length):
            painter.drawLine(0, y, panel_width, y)

        painter.setPen(self.screen_pen)

        if level.is_vertical:
            for y in range(0, panel_height, self.block_length * SCREEN_HEIGHT):
                painter.drawLine(0, self.block_length + y, panel_width, self.block_length + y)
        else:
            for x in range(0, panel_width, self.block_length * SCREEN_WIDTH):
                painter.drawLine(x, 0, x, panel_height)

    def _draw_auto_scroll(self, painter: QPainter, level: Level):
        for item in level.enemies:
            if item.obj_index == OBJ_AUTOSCROLL:
                break
        else:
            return

        drawer = AutoScrollDrawer(item.y_position, level)

        drawer.draw(painter, self.block_length)
