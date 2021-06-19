from typing import Hashable, Callable, Optional
from collections import deque


class UndoRedo:
    def __init__(
        self,
        callable: Callable,
        current_state: Hashable = None,
        undo_stack: Optional[deque] = None,
        redo_stack: Optional[deque] = None,
    ):
        self._current = current_state
        self._undo = undo_stack or deque()
        self._redo = redo_stack or deque()
        self._callable = callable

    @property
    def current(self) -> Hashable:
        return self._current

    @current.setter
    def current(self, state: Hashable):
        self._current = state
        self._callable(self._current)

    @property
    def can_undo(self) -> bool:
        return len(self._undo) != 0

    @property
    def can_redo(self) -> bool:
        return len(self._redo) != 0

    def append(self, state: Hashable):
        self._undo.append(self._current)
        self._redo.clear()
        self.current = state

    def clear(self, state: Hashable):
        self._undo.clear()
        self._redo.clear()
        self.current = state

    def safe_undo(self):
        if self.can_undo:
            self.undo()

    def undo(self):
        assert self.can_undo
        self._redo.append(self._current)
        self.current = self._undo.pop()

    def safe_redo(self):
        if self.can_redo:
            self.redo()

    def redo(self):
        assert self.can_redo
        self._undo.append(self._current)
        self.current = self._redo.pop()
