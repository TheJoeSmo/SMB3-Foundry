from abc import ABC

from core.File import File
from core.FileManager.AbstractHandler import AbstractHandler
from core.FileManager.FileHandlerClosedException import FileHandlerClosedException


class AbstractFileHandlerMeta(AbstractHandler, ABC):
    """Provides a series of helper functions to generate a file"""
    def __init__(self, file: File, data: bytearray, **kwargs) -> None:
        self.file = file
        self._data = data

    @property
    def data(self) -> bytearray:
        """The contents of the file in the form of a bytearray"""
        if self._data is None:
            raise FileHandlerClosedException(self)
        return self._data

    @property
    def program_banks(self) -> int:
        """The amount of program banks"""
        return self.data[4]

    @property
    def character_banks(self) -> int:
        """The amount of character banks"""
        return self.data[5]

    def close(self):
        self._data = None  # Remove the data