from typing import Dict, List, Iterable, Callable
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from cached_property import cached_property

from core.BlockGroup import BlockGroup

from core.FileManager.AbstractHandler import AbstractHandler
from core.FileManager.AbstractPassableHandler import AbstractPassableHandler
from core.FileManager.FileHandlerMeta import FileHandlerMeta


HandlerConstructor = Callable[[AbstractHandler], AbstractHandler]


class AbstractBlockGroupHandler(AbstractPassableHandler, ABC):
    """Provide a series of helper functions to generate block groups for a file"""
    def __init__(self, handler: FileHandlerMeta, handlers: Dict[str, HandlerConstructor]):
        self.handler = handler
        super().__init__(handlers={name: handler(self) for name, handler in handlers.items()})

    def generate(self, session: Session, **kwargs) -> None:
        """Generates a series of block groups and call the respective handlers for it"""
        for block_group in self.block_groups:
            session.add(block_group)

        for handler in self.handlers:
            handler.generate(session)

    @property
    @abstractmethod
    def tileset_offsets(self) -> Iterable[int]:
        """Finds a series of indexes into the respective tilesets"""

    @property
    @abstractmethod
    def tileset_names(self) -> Iterable[int]:
        """Finds a series of names for the respective tilesets"""

    @cached_property
    def block_groups(self) -> List[BlockGroup]:
        return [
            BlockGroup(file_id=self.handler.file.id, name=name, offset=offset)
            for name, offset in zip(self.tileset_names, self.tileset_offsets)
        ]
