from typing import Callable, Dict

from sqlalchemy.orm import Session

from core.File import File

from core.FileManager.AbstractHandler import AbstractHandler
from core.FileManager.AbstractPassableHandler import AbstractPassableHandler
from core.FileManager.AbstractFileHandlerMeta import AbstractFileHandlerMeta


HandlerConstructor = Callable[[AbstractHandler], AbstractHandler]


class FileHandlerMeta(AbstractPassableHandler, AbstractFileHandlerMeta):
    """Handle the data inside the file and the generation of various other constructors determine at initialization"""
    def __init__(self, handlers: Dict[str, HandlerConstructor], file: File, data: bytearray):
        super().__init__(handlers={name: handler(self) for name, handler in handlers.items()}, file=file, data=data, )

    def generate(self, session: Session, **kwargs) -> None:
        for handler in self.handlers:
            handler.generate(session)
