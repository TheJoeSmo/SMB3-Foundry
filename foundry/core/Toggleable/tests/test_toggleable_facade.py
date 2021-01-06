

import pytest

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException
from foundry.core.Toggleable.Toggleable import Toggleable
from foundry.core.Toggleable.ToggleableFacade import ToggleableFacade


def enable():
    return True


def disable():
    return False


class State:
    def __init__(self):
        self.state = None

    def __call__(self, state: bool) -> bool:
        self.state = state
        return True


def test_initialization():
    ToggleableFacade(Toggleable(enable, disable))


def test_uninitialized_state_exception():
    toggleable = ToggleableFacade(Toggleable(enable, disable))
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state_from_init():
    toggleable = ToggleableFacade(Toggleable(enable, disable, True))
    assert toggleable._toggleable._state


def test_setting_state():
    toggleable = ToggleableFacade(Toggleable(enable, disable))
    toggleable.state = True
    assert toggleable._toggleable._state


def test_getting_state():
    toggleable = ToggleableFacade(Toggleable(enable, disable, True))
    toggleable.state = not toggleable._toggleable.state
    assert not toggleable.state
