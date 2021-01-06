

from typing import Optional
from abc import abstractmethod

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException


class AbstractToggleable:
    """
    An interface for a toggleable object that can be turned on or off and retains state.
    """

    def __init__(self, state: Optional[bool] = None, **kwargs):
        self._state = state

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._state})"

    @property
    def state(self) -> bool:
        """
        The state of the object
        :return: True if the object is enabled; False if the object is disabled
        """
        if self._state is None:
            raise UninitializedStateException
        return self._state

    @state.setter
    def state(self, state: bool) -> None:
        self._state = state

    @abstractmethod
    def enable(self, *args, **kwargs) -> bool:
        """
        Enables the state
        :return: if the state enabled properly
        """

    @abstractmethod
    def disable(self, *args, **kwargs) -> bool:
        """
        Disables the state
        :return: if the state disabled properly
        """
