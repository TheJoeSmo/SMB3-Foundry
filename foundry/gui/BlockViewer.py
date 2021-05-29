from typing import Callable

from PySide2.QtCore import QPoint, QRect, QSize
from PySide2.QtGui import QBrush, QMouseEvent, QPaintEvent, QPainter, QResizeEvent, Qt
from PySide2.QtWidgets import QComboBox, QLabel, QLayout, QStatusBar, QToolBar, QWidget, QSizePolicy

from foundry import icon

from foundry.core.TileSquareAssembly import get_tsa_offset
from foundry.core.TileSquareAssembly.Block import Block as MetaBlock

from foundry.game.gfx.GraphicsSet import GraphicsSet
from foundry.game.gfx.Palette import PALETTE_GROUPS_PER_OBJECT_SET, bg_color_for_object_set, load_palette_group
from foundry.game.gfx.drawable.Tile import Tile
from foundry.game.gfx.drawable.Block import Block, clear_block_cache

from foundry.gui.tsa_data import get_controller
from foundry.gui.CustomChildWindow import CustomChildWindow
from foundry.gui.LevelSelector import OBJECT_SET_ITEMS
from foundry.gui.Spinner import Spinner
from foundry.gui.CustomDialog import CustomDialog as Dialog


class BlockViewer(CustomChildWindow):
    def __init__(self, parent, level_ref):
        super(BlockViewer, self).__init__(parent, "Block Viewer")
        self.controller = get_controller()
        self.level_ref = level_ref  # For reloading

        self._object_set = 0
        self.block_viewer = BlockBank(parent=self)

        self.setCentralWidget(self.block_viewer)

        self.toolbar = QToolBar(self)

        self.prev_os_action = self.toolbar.addAction(icon("arrow-left.svg"), "Previous object set")
        self.prev_os_action.triggered.connect(self.prev_object_set)

        self.next_os_action = self.toolbar.addAction(icon("arrow-right.svg"), "Next object set")
        self.next_os_action.triggered.connect(self.next_object_set)

        self.zoom_out_action = self.toolbar.addAction(icon("zoom-out.svg"), "Zoom Out")
        self.zoom_out_action.triggered.connect(self.block_viewer.zoom_out)

        self.zoom_in_action = self.toolbar.addAction(icon("zoom-in.svg"), "Zoom In")
        self.zoom_in_action.triggered.connect(self.block_viewer.zoom_in)

        self.bank_dropdown = QComboBox(parent=self.toolbar)
        self.bank_dropdown.addItems(OBJECT_SET_ITEMS)
        self.bank_dropdown.setCurrentIndex(0)

        self.bank_dropdown.currentIndexChanged.connect(self.on_combo)

        self.palette_group_spinner = Spinner(self, maximum=PALETTE_GROUPS_PER_OBJECT_SET - 1, base=10)
        self.palette_group_spinner.valueChanged.connect(self.on_palette)

        self.toolbar.addWidget(self.bank_dropdown)
        self.toolbar.addWidget(QLabel(" Object Palette: "))
        self.toolbar.addWidget(self.palette_group_spinner)

        self.addToolBar(self.toolbar)

        self.block_editor_tool_bar = QToolBar("Block Editor", self)
        self.block_editor_tool_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.block_editor_tool_bar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.block_editor_tool_bar.setFloatable(True)
        self.block_editor_tool_bar.setAllowedAreas(Qt.LeftToolBarArea | Qt.RightToolBarArea)
        self.block_editor = BlockEditor(parent=self, index=0)
        self.block_editor_tool_bar.addWidget(self.block_editor)
        self.addToolBar(Qt.RightToolBarArea, self.block_editor_tool_bar)

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.setStatusBar(QStatusBar(self))

        return

    @property
    def object_set(self):
        return self._object_set

    @object_set.setter
    def object_set(self, value):
        self._object_set = value

        self._after_object_set()

    @property
    def palette_group(self):
        return self.palette_group_spinner.value()

    @palette_group.setter
    def palette_group(self, value):
        self.palette_group_spinner.setValue(value)

    def prev_object_set(self):
        self.object_set = max(self.object_set - 1, 0)

    def next_object_set(self):
        self.object_set = min(self.object_set + 1, 0xE)

    def _after_object_set(self):
        self.block_viewer.object_set = self.object_set
        self.block_editor.object_set = self.object_set

        self.bank_dropdown.setCurrentIndex(self.object_set)

        self.block_editor.update()
        self.block_viewer.update()

    def on_combo(self, _):
        self.object_set = self.bank_dropdown.currentIndex()

        self.block_viewer.object_set = self.object_set
        self.block_editor.object_set = self.object_set

        self.block_editor.update()
        self.block_viewer.update()

    def on_palette(self, value):
        self.block_viewer.palette_group = value
        self.block_editor.palette_group = value
        self.block_viewer.update()
        self.block_editor.update()

    def on_index(self, index: int):
        self.block_editor.index = index
        self.block_editor.update()

    def on_tsa_update(self):
        self.block_viewer.update()
        self.block_editor.update()
        self.level_ref.reload()


class TileBank(Dialog):
    def __init__(
        self,
        parent,
        title="Select a Tile",
        object_set=0,
        palette_index=0,
        palette_group=0,
        zoom=2,
        return_func: Callable = None,
    ):
        super(TileBank, self).__init__(parent, title)
        self.real_parent = parent
        self.setMouseTracking(True)

        self.controller = get_controller()
        self.object_set = object_set
        self.palette_index = palette_index
        self.palette_group = palette_group
        self.zoom = zoom
        self.return_func = return_func

        self._size = self._get_size()
        self.setFixedSize(self._size)

    def resizeEvent(self, event: QResizeEvent):
        self.update()

    def zoom_in(self):
        self.zoom += 1
        self._after_zoom()

    def zoom_out(self):
        self.zoom = max(self.zoom - 1, 1)
        self._after_zoom()

    def _get_size(self):
        return QSize(32 * Tile.WIDTH * self.zoom, 32 * Tile.HEIGHT * self.zoom)

    def _after_zoom(self):
        new_size = self._get_size()

        self.setFixedSize(new_size)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x, y = event.pos().toTuple()

        block_length = Block.WIDTH * self.zoom

        column = x // block_length
        row = y // block_length

        index = row * 16 + column

        if self.return_func is not None:
            self.return_func(index)

        self.close()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        bg_color = bg_color_for_object_set(self.object_set, 0)
        painter.setBrush(QBrush(bg_color))

        painter.drawRect(QRect(QPoint(0, 0), self.size()))

        graphics_set = GraphicsSet(self.object_set)
        palette = load_palette_group(self.object_set, self.palette_group)

        tile_length = Tile.WIDTH * self.zoom * 2

        for i in range(0x100):
            tile = Tile(i, palette, self.palette_index, graphics_set)

            x = (i % 16) * tile_length
            y = (i // 16) * tile_length

            tile.draw(painter, x, y, tile_length)

        return


class BlockEditor(QWidget):
    def __init__(self, parent, object_set=0, palette_group=0, zoom=2, index=0):
        super(BlockEditor, self).__init__(parent)
        self.real_parent = parent
        self.setMouseTracking(True)

        self.controller = get_controller()
        self.object_set = object_set
        self.palette_group = palette_group
        self.zoom = zoom
        self.index = index

        self._size = self._get_size()
        self.setFixedSize(self._size)

    def resizeEvent(self, event: QResizeEvent):
        self.update()

    def zoom_in(self):
        self.zoom += 1
        self._after_zoom()

    def zoom_out(self):
        self.zoom = max(self.zoom - 1, 1)
        self._after_zoom()

    def _get_size(self):
        return QSize(2 * Block.WIDTH * self.zoom, 2 * Block.HEIGHT * self.zoom)

    def _after_zoom(self):
        new_size = self._get_size()

        self.setFixedSize(new_size)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x, y = event.pos().toTuple()

        tile_length = Block.WIDTH * self.zoom

        column = x // tile_length
        row = y // tile_length

        tile = row + column * 2

        def return_func(index):
            tsa_offset = get_tsa_offset(self.object_set)
            tsa = None
            for _tsa in self.controller.rom.tile_square_assemblies:
                if tsa_offset == _tsa.tsa_offset:
                    tsa = _tsa
                    break
            if tsa is None:
                raise KeyError(f"No tile square assembly is found at {tsa_offset}")
            blocks = tsa.blocks
            patterns = list(blocks[self.index].patterns)
            patterns[tile] = index
            block = MetaBlock.from_data(None, *patterns)
            blocks[self.index] = block
            tsa.blocks = blocks
            clear_block_cache()
            self.real_parent.on_tsa_update()

        TileBank(
            self,
            object_set=self.object_set,
            palette_group=self.palette_group,
            palette_index=self.index // 0x40,
            zoom=self.zoom,
            return_func=return_func,
        ).exec_()

        return super().mousePressEvent(event)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        bg_color = bg_color_for_object_set(self.object_set, 0)
        painter.setBrush(QBrush(bg_color))

        painter.drawRect(QRect(QPoint(0, 0), self.size()))

        graphics_set = GraphicsSet(self.object_set)
        palette = load_palette_group(self.object_set, self.palette_group)

        tsa_offset = get_tsa_offset(self.object_set)
        tsa = None
        for _tsa in self.controller.rom.tile_square_assemblies:
            if tsa_offset == _tsa.tsa_offset:
                tsa = _tsa
                break
        if tsa is None:
            raise KeyError(f"No tile square assembly is found at {tsa_offset}")

        tsa_data = tsa.to_bytes()

        block_length = 2 * Block.WIDTH * self.zoom

        block = Block(self.index, palette, graphics_set, tsa_data)

        block.draw(painter, 0, 0, block_length)


class BlockBank(QWidget):
    def __init__(self, parent, object_set=0, palette_group=0, zoom=2):
        super(BlockBank, self).__init__(parent)
        self.real_parent = parent
        self.setMouseTracking(True)

        self.controller = get_controller()
        self.object_set = object_set
        self.palette_group = palette_group
        self.zoom = zoom

        self._size = self._get_size()
        self.setFixedSize(self._size)

    def resizeEvent(self, event: QResizeEvent):
        self.update()

    def zoom_in(self):
        self.zoom += 1
        self._after_zoom()

    def zoom_out(self):
        self.zoom = max(self.zoom - 1, 1)
        self._after_zoom()

    def _get_size(self):
        return QSize(16 * Block.WIDTH * self.zoom, 16 * Block.HEIGHT * self.zoom)

    def _after_zoom(self):
        new_size = self._get_size()

        self.setFixedSize(new_size)

    def mouseMoveEvent(self, event: QMouseEvent):
        x, y = event.pos().toTuple()

        block_length = Block.WIDTH * self.zoom

        column = x // block_length
        row = y // block_length

        dec_index = row * 16 + column
        hex_index = hex(dec_index).upper().replace("X", "x")

        status_message = f"Row: {row}, Column: {column}, Index: {dec_index} / {hex_index}"

        self.parent().statusBar().showMessage(status_message)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        x, y = event.pos().toTuple()

        block_length = Block.WIDTH * self.zoom

        column = x // block_length
        row = y // block_length

        index = row * 16 + column

        self.real_parent.on_index(index)

        return super().mousePressEvent(event)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        bg_color = bg_color_for_object_set(self.object_set, 0)
        painter.setBrush(QBrush(bg_color))

        painter.drawRect(QRect(QPoint(0, 0), self.size()))

        graphics_set = GraphicsSet(self.object_set)
        palette = load_palette_group(self.object_set, self.palette_group)

        tsa_offset = get_tsa_offset(self.object_set)
        tsa = None
        for _tsa in self.controller.rom.tile_square_assemblies:
            if tsa_offset == _tsa.tsa_offset:
                tsa = _tsa
                break
        if tsa is None:
            raise KeyError(f"No tile square assembly is found at {tsa_offset}")

        tsa_data = tsa.to_bytes()

        block_length = Block.WIDTH * self.zoom

        for i in range(0x100):
            block = Block(i, palette, graphics_set, tsa_data)

            x = (i % 16) * block_length
            y = (i // 16) * block_length

            block.draw(painter, x, y, block_length)

        return
