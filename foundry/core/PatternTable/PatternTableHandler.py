

from foundry.core.PatternTable import CHR_PAGE
from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.PatternTable.ObservablePatternTable import ObservablePatternTable
from foundry.game.File import ROM


def _chr_offset() -> int:
    """
    Get the correct offset into the ROM for the graphics
    """
    return ROM().get_byte(5) * 0x4000 + 0x10


class PatternTableHandler:
    """Makes an artificial PPU for the graphics"""
    def __init__(self, pattern_table: PatternTable):
        self._pattern_table = ObservablePatternTable.from_pattern_table(pattern_table)

        # Have a check to automatically update the data when needed
        self._data = bytearray()
        self.needs_updating = True
        self.pattern_table.update_observable.attach_observer(lambda *_: setattr(self, "needs_updating", True))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pattern_table}) with data {self.data}"

    @property
    def pattern_table(self) -> ObservablePatternTable:
        return self._pattern_table

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTable) -> None:
        self._pattern_table.pattern_table = pattern_table

    @property
    def data(self):
        if self.needs_updating:
            data = bytearray()
            offset = _chr_offset()
            for i in range(4):
                data.extend(ROM().bulk_read(CHR_PAGE, offset + CHR_PAGE * self.pattern_table[i]))
            self._data = data
            self.needs_updating = False
        return self._data

    @property
    def number(self) -> int:
        """for legacy reasons"""
        return 0
