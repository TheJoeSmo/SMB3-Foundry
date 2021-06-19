from copy import copy
from typing import Callable

from foundry.core.Saver.SmartSaver import SmartSaver
from foundry.core.Saver.Verifier import Verifier


class SaverManager:
    def __init__(
        self,
        primary: SmartSaver,
        verifier: Verifier,
        file_func: Callable,
    ):
        self._main = primary
        self.verifier = verifier
        self.file_func = file_func
        self.main = self.initialize()
        self.update()

    @property
    def main(self) -> SmartSaver:
        """
        The primary saver that holds the current, saved version, of the item.
        """
        return self._main

    @main.setter
    def main(self, main: SmartSaver):
        self._main.from_copy(main)  # We never override main, as it is the only non-temporary saver
        self._main.delete_temp()
        self.working = copy(main)

    @property
    def has_changes(self) -> bool:
        """
        Determines if the saved item has changes between the working and non-working branches.
        """
        return not self.verifier.is_like(self.main, self.working)

    def apply_underlying_changes(self) -> SmartSaver:
        """
        Applies the changes to the saver and also checks if any changes were made to the saved copy.
        """
        from_file: SmartSaver = self.file_func()
        if not self.verifier.is_like(self.main, from_file):
            return self.verifier.resolution(self.main, from_file)
        else:
            return copy(self.main)

    def initialize(self):
        """
        Initialize the data and check if any changes were made between sessions.
        """
        from_file: SmartSaver = self.file_func()
        if self.verifier.is_like(from_file, self.main):
            return self.main  # Favor data as it would have custom user information
        else:
            return self.verifier.resolution(self.main, from_file)

    def update(self):
        """
        Applies the changes from working to main and checks for any underlying changes.
        """
        temp_main = self.apply_underlying_changes()
        self.main = self.verifier.apply(temp_main, self.working)

    def import_new(self, saver: SmartSaver):
        """
        Imports a new saver to the working branch.
        """
        self.working = saver
