from abc import ABC

from foundry.core.Saver.Saver import Saver


class SmartSaver(Saver, ABC):
    @staticmethod
    def delete_temp():
        """
        Remove all temporary elements
        """
