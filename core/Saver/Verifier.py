from abc import ABC, abstractmethod

from core.Saver.Saver import Saver


class Verifier(ABC):
    @abstractmethod
    def is_like(self, primary: Saver, secondary: Saver) -> bool:
        """
        Determines if two savers are similar enough to one another to be considered the same.
        """

    @abstractmethod
    def resolution(self, primary: Saver, secondary: Saver) -> Saver:
        """
        Resolves the conflict, by choosing one of the two.
        """

    @abstractmethod
    def apply(self, primary: Saver, secondary: Saver) -> Saver:
        """
        Applies data from one saver to another.  Primary will attempt to write its data ontop of secondary.
        """
