from typing import List

from sqlalchemy.orm import Session

from core.PatternTable import PatternTable

from core.FileManager.AbstractHandler import AbstractHandler
from core.FileManager.FileHandlerMeta import FileHandlerMeta


class PatternTableHandler(AbstractHandler):
    """Provide a series of helper functions to generate pattern tables for a file"""
    def __init__(self, handler: FileHandlerMeta):
        self.handler = handler

    def generate(self, session: Session, **kwargs) -> None:
        """Generates a series of pattern tables"""
        for pattern_table in self.pattern_tables:
            session.add(pattern_table)

    @cached_property
    def pattern_tables(self) -> List[PatternTable]:
        return [PatternTable(file_id=self.handler.file.id, index=i) for i in range(self.handler.character_banks)]
