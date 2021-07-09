from typing import Callable

from core.FileManager.AbstractFileHandlerMeta import AbstractFileHandlerMeta


OffsetModifier = Callable[[int, int], int]


class OffsetIterator:
    """An iterator that finds all the tileset offsets and stops when it reads a specific byte"""
    def __init__(self, file: AbstractFileHandlerMeta, offset: int, func: OffsetModifier, stop_byte: int):
        self.file = file
        self.offset = offset
        self.func = func
        self.stop_byte = stop_byte
        self.iterations = 0

    def __iter__(self):
        return self

    def __next__(self):
        offset = self.func(self.file.data[self.offset + self.iterations], self.iterations)
        if offset == self.stop_byte:
            raise StopIteration()
        self.iterations += 1
        return offset
