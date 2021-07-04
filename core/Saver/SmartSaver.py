from abc import ABC

from core.Saver.Saver import Saver


class SmartSaver(Saver, ABC):
    @staticmethod
    def delete_temp():
        """
        Remove all temporary elements
        """
