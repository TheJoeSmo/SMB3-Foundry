from abc import ABC, abstractmethod


class Saver(ABC):
    @property
    @abstractmethod
    def data(self):
        """
        Saves the data to a tuple to be compared.
        """

    @abstractmethod
    def from_copy(self, copy: "Saver"):
        """
        Applies data from a copy
        """
