

import pytest

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException
from foundry.core.Toggleable.AbstractToggleable import AbstractToggleable


class GenericToggleable(AbstractToggleable):
    def enable(self, *args, **kwargs) -> bool:
        return True

    def disable(self, *args, **kwargs) -> bool:
        return True


def test_initialization():
    GenericToggleable()


def test_uninitialized_state_exception():
    toggleable = GenericToggleable()
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state():
    toggleable = GenericToggleable()
    toggleable.state = True
    assert toggleable._state


def test_getting_state():
    toggleable = GenericToggleable()
    toggleable.state = True
    toggleable.state = not toggleable.state
    assert not toggleable.state
