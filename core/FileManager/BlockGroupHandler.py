from typing import List, Dict, Iterable

from cached_property import cached_property

from smb3parse.constants import PAGE_A000_ByTileset, WORLD_MAP_TSA_INDEX

from core.BlockGroup import BlockGroup

from core.FileManager.AbstractBlockGroupHandler import AbstractBlockGroupHandler, HandlerConstructor
from core.FileManager.FileHandlerMeta import FileHandlerMeta
from core.FileManager.OffsetIterator import OffsetModifier, OffsetIterator


class BlockGroupHandler(AbstractBlockGroupHandler):
    """Provide a series of helper functions to generate block groups for a file"""
    def __init__(
            self,
            handler: FileHandlerMeta,
            handlers: Dict[str, HandlerConstructor],
            offset_start: int = PAGE_A000_ByTileset,
            offset_modifier: OffsetModifier = lambda result, idx: WORLD_MAP_TSA_INDEX if not idx else result,
            offset_end_byte: int = 0x60
    ):
        self.offset_start = offset_start
        self.offset_modifier = offset_modifier
        self.offset_end_byte = offset_end_byte
        super().__init__(handler=handler, handlers=handlers)

    @property
    def tileset_offsets(self) -> Iterable[int]:
        """Finds a series of indexes into the respective tilesets"""
        return OffsetIterator(self.handler.file, self.offset_start, self.offset_modifier, self.offset_end_byte)

    @property
    def tileset_names(self) -> Iterable[str]:
        """Finds a series of names for the respective tilesets"""
        class NameIterator:
            def __init__(self):
                self.count = -1

            def __iter__(self):
                return self

            def __next__(self):
                self.count += 1
                return f"Tileset_{self.count}"

        return NameIterator()

    @cached_property
    def block_groups(self) -> List[BlockGroup]:
        """Remove duplicates, as we do not want those"""
        return list(set(super().block_groups))
