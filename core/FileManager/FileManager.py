from typing import Optional, List

from core import session
from core.File import File
from core.PatternTable import PatternTable
from core.BlockGroup import BlockGroup

from smb3parse.constants import PAGE_A000_ByTileset


class ROM:
    """Provides useful ROM information from a given path"""

    def __init__(self, file: File):
        self.file = file

        with open(self.file.path, "rb") as rom:
            self.data = bytearray(rom.read())

    @property
    def program_banks(self) -> int:
        """The amount of program banks"""
        return self.data[4]

    @property
    def character_banks(self) -> int:
        """The amount of character banks"""
        return self.data[5]

    def get_tilesets(self, start_byte=PAGE_A000_ByTileset, end_byte=0x60) -> bytearray:
        """Provides a list of bytes, corresponding with the tilesets"""
        return self.data[start_byte: self.data[start_byte:].index(end_byte)]

    def create_pattern_tables(self):
        """Create every pattern table inside the ROM and add them to the file"""
        map(session.add, [PatternTable(file_id=self.file.id, index=i) for i in range(self.character_banks)])

    def create_block_groups(self):
        """Create every block group inside the ROM and add them to the file"""
        for tileset in set(self.get_tilesets()):
            block_group = BlockGroup(file_id=self.file.id, offset=tileset)


class FileManager:
    """Manages a File to connect it with the actual ROM provided"""

    def __init__(self, main: Optional[File]):
        self.main = main or File(name=None)
        self.version = None
        session.add(self.main)
        self.commit()

    @classmethod
    def from_file(cls):
        """"""

    def commit(self):
        """Commit a change and update the revert changes to this state"""
        self.version = self.main.versions[-1]  # Get the last version
        session.commit()

    def revert(self):
        """Revert to the last commit"""
        self.version.revert()
        session.commit()
