from core.File import File
from core.FileManager.FileHandlerMeta import FileHandlerMeta


class FileHandler:
    """Gathers data from a given file and provide a series of helper functions"""
    def __init__(self, file: File):
        self.file = file
        self.handler = None

    def __enter__(self) -> FileHandlerMeta:
        with open(self.file.path, "rb") as rom:
            self.handler = FileHandlerMeta(self.file, bytearray(rom.read()))
        return self.handler

    def __exit__(self, type, value, traceback) -> None:
        self.handler.close()
