

from foundry.core.PatternTable.PatternTable import PatternTable
from foundry.core.Observables.GenericObservable import GenericObservable


class ObservablePatternTable(PatternTable):
    """A pattern table that provides updates"""
    def __init__(
            self,
            page_0: int,
            page_1: int,
            page_2: int,
            page_3: int,
    ):
        self._pattern_table = PatternTable(page_0, page_1, page_2, page_3)

        self.update_observable = GenericObservable("update")
        self.page_update_observable = GenericObservable("page_update")
        self.page_update_observable.attach_observer(lambda *_: self.update_observable.notify_observers())

    def __setitem__(self, key: int, value: int):
        # Note, if you update the pattern table by setting it in a list, you will cause more updates
        # It is better to send a new palette set, so only one update occurs
        pattern_table = self.pattern_table
        pattern_table[key] = value
        self.pattern_table = pattern_table

    @property
    def page_0(self) -> int:
        return self._pattern_table.page_0

    @page_0.setter
    def page_0(self, page: int) -> None:
        pattern_table = self.pattern_table
        pattern_table.page_0 = page
        self.pattern_table = pattern_table

    @property
    def page_1(self) -> int:
        return self._pattern_table.page_1

    @page_1.setter
    def page_1(self, page: int) -> None:
        pattern_table = self.pattern_table
        pattern_table.page_1 = page
        self.pattern_table = pattern_table

    @property
    def page_2(self) -> int:
        return self._pattern_table.page_2

    @page_2.setter
    def page_2(self, page: int) -> None:
        pattern_table = self.pattern_table
        pattern_table.page_2 = page
        self.pattern_table = pattern_table

    @property
    def page_3(self) -> int:
        return self._pattern_table.page_3

    @page_3.setter
    def page_3(self, page: int) -> None:
        pattern_table = self.pattern_table
        pattern_table.page_3 = page
        self.pattern_table = pattern_table

    @property
    def pattern_table(self) -> PatternTable:
        return PatternTable(self.page_0, self.page_1, self.page_2, self.page_3)

    @pattern_table.setter
    def pattern_table(self, pattern_table: PatternTable) -> None:
        if self.pattern_table != pattern_table:
            for i, page in enumerate(pattern_table):
                self._pattern_table[i] = page
            self.page_update_observable.notify_observers(self.pattern_table)
