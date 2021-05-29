from PySide2.QtWidgets import QWidget
import time

from foundry.game.File import ROM as File

from foundry.gui.ROMResolver import ROMResolver

from foundry.core.Saver.SaverManager import SaverManager

from foundry.core.TileSquareAssembly.ROM import ROM
from foundry.core.TileSquareAssembly.Saver.ROMVerifier import ROMVerifier


_refresh_rate = 2


class Controller:
    def __init__(self, parent: QWidget, rom_name: str):
        self.parent = parent
        self.saver = None
        self._time_to_update_has_changes = None
        self._has_changes_last_value = None
        self.load_new_rom(rom_name)

    @property
    def has_changes(self) -> bool:
        """ "
        Returns if the working address has changes that are unsaved.
        """
        if (
            self._has_changes_last_value is None
            or self._time_to_update_has_changes is None
            or self._time_to_update_has_changes < time.time()
        ):
            self._time_to_update_has_changes = time.time() + _refresh_rate
            self._has_changes_last_value = self.saver.has_changes
        return self._has_changes_last_value

    @property
    def rom(self):
        """
        Returns the working ROM of the saver.
        """
        return self.saver.working

    def load_new_rom(self, rom_name: str):
        """
        Reloads the ROM currently in main and working of the saver.
        """

        def check_current_rom(*_):
            File.reload()  # Reload the rom, to check if there are any changes
            return ROM.from_rom(None)

        self.saver = SaverManager(ROM.from_name(rom_name), ROMVerifier(ROMResolver(self.parent)), check_current_rom)

    def save(self):
        """
        Saves the changes to the ROM currently loaded.
        """
        self.saver.update()
        self.saver.main.apply_to_rom()

    def import_new(self, rom: ROM):
        """
        Imports the new changes to the working ROM.
        """
        self.saver.import_new(rom)
