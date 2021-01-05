

from typing import Final
from abc import abstractmethod


class AbstractPlugin:
    """
    An interface of what a Plugin should be
    """

    def __init__(self, name: str, **kwargs) -> None:
        self._name: Final[str] = name

    @property
    def name(self) -> str:
        """A property for accessing name, """
        return self._name

    @abstractmethod
    def create(self) -> bool:
        """
        Creates any extra dependencies required for the plugin.
        :return: a bool depending if it created these dependencies successfully
        """

    @abstractmethod
    def delete(self) -> bool:
        """
        Delete itself and any dependencies that will not be needed
        :return: a bool depending if it deleted these dependencies successfully
        """

    @abstractmethod
    def enable(self) -> bool:
        """
        Enables itself and handles any other requirements that are needed
        :return: a bool depending if it enabled itself successfully
        """

    @abstractmethod
    def disable(self) -> bool:
        """
        Disable itself and handles any other disabling required
        :return: a bool depending if it disabled itself successfully
        """