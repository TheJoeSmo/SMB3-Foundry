class FileHandlerClosedException(Exception):
    """An exception that is raised when the file handler has already been closed, but was called"""
    def __init__(self, handler):
        self.handler = handler
        super(self).__init__()