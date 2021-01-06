

import pytest

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException
from foundry.core.Toggleable.AbstractToggleable import AbstractToggleable


class GenericToggleable(AbstractToggleable):
    def enable(self, *args, **kwargs) -> bool:
        self.value = True
        return True

    def disable(self, *args, **kwargs) -> bool:
        self.value = False
        return True


def test_initialization():
    GenericToggleable()


def test_uninitialized_state_exception():
    toggleable = GenericToggleable()
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state_from_init():
    toggleable = GenericToggleable(True)
    assert toggleable._state


def test_setting_state():
    toggleable = GenericToggleable()
    toggleable.state = True
    assert toggleable._state


def test_getting_state():
    toggleable = GenericToggleable(True)
    toggleable.state = not toggleable.state
    assert not toggleable.state


def test_state_enable():
    toggleable = GenericToggleable(True)
    assert toggleable.value


def test_state_disable():
    toggleable = GenericToggleable(False)
    assert not toggleable.value
