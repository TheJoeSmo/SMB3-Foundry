from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QPen, Qt

from foundry.game.gfx.drawable.Block import Block
from foundry.game.gfx.objects.LevelObject import SCREEN_HEIGHT, SCREEN_WIDTH
from foundry.game.level.WorldMap import WorldMap


class WorldDrawer:
    def __init__(self):
        self.draw_level_pointers = True
        self.draw_sprites = True
        self.draw_start = True
        self.draw_airship_points = True
        self.draw_pipes = True
        self.draw_locks = True

        self.block_length = Block.WIDTH

        self.grid_pen = QPen(QColor(0x80, 0x80, 0x80, 0x80), 1)
        self.screen_pen = QPen(QColor(0xFF, 0x00, 0x00, 0xFF), 1)

    def draw(self, painter: QPainter, world: WorldMap):
        self._draw_background(painter, world)

        self._draw_grid(painter, world)

        self._draw_tiles(painter, world)

        if self.draw_level_pointers:
            # TODO: Fix and understand rules on where pointers can be
            self._draw_level_pointers(painter, world)

        if self.draw_sprites:
            self._draw_sprites(painter, world)

        if self.draw_start:
            self._draw_start_position(painter, world)

        self.draw_airship_points = True
        self.draw_pipes = True
        self.draw_locks = True

    def _draw_background(self, painter: QPainter, world: WorldMap):
        painter.save()

        bg_color = Qt.black

        painter.fillRect(world.get_rect(self.block_length), bg_color)

        painter.restore()

    def _draw_grid(self, painter: QPainter, world: WorldMap):
        painter.save()

        painter.setPen(QPen(Qt.gray, 1))

        # rows
        map_length = SCREEN_WIDTH * self.block_length * world.internal_world_map.screen_count

        for y in range(SCREEN_HEIGHT):
            y *= self.block_length

            painter.drawLine(QPoint(0, y), QPoint(map_length, y))

        # columns
        for x in range(SCREEN_WIDTH * world.internal_world_map.screen_count):
            x *= self.block_length

            painter.drawLine(QPoint(x, 0), QPoint(x, SCREEN_HEIGHT * self.block_length))

        painter.restore()

    def _draw_tiles(self, painter: QPainter, world: WorldMap):
        for tile in world.get_all_objects():
            tile.render()

            tile.draw(painter, self.block_length, False)

            if tile.selected:
                painter.save()

                painter.setPen(QPen(QColor(0x00, 0x00, 0x00, 0x80), 1))
                painter.drawRect(tile.get_rect(self.block_length))

                painter.restore()

    def _draw_level_pointers(self, painter: QPainter, world: WorldMap):
        painter.save()

        for index, level_pointer in enumerate(world.level_pointers):
            selected = index in world.selected_level_pointers

            level_pointer.draw(painter, self.block_length, False, selected)

        painter.restore()

    def _draw_sprites(self, painter: QPainter, world: WorldMap):
        painter.save()

        for sprite in world.sprites:
            selected = sprite.data.index in world.selected_sprites

            sprite.draw(painter, self.block_length, False, selected)

        painter.restore()

    def _draw_start_position(self, painter: QPainter, world: WorldMap):
        painter.save()

        start_pos = world.internal_world_map.start_pos

        if start_pos is None:
            return

        world, screen, y, x = start_pos.tuple()

        x *= self.block_length
        y *= self.block_length

        painter.fillRect(
            QRect(QPoint(x, y), QSize(self.block_length, self.block_length)), QColor(0x00, 0x00, 0xFF, 0x80)
        )

        painter.restore()