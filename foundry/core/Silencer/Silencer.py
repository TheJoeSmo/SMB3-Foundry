

from typing import Callable


class Silencer:
    """Stops, silences, a function from running if it is set"""

    def __init__(self, func: Callable, silenced: bool = False):
        self.func, self.silenced = func, silenced

    def __call__(self, *args, **kwargs):
        if not self.silenced:
            self.func(*args, **kwargs)
