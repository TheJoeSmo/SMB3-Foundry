

import pytest

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException
from foundry.core.Toggleable.Toggleable import Toggleable


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
    Toggleable(enable, disable)


def test_uninitialized_state_exception():
    toggleable = Toggleable(enable, disable)
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state_from_init():
    toggleable = Toggleable(enable, disable, True)
    assert toggleable._state


def test_setting_state():
    toggleable = Toggleable(enable, disable)
    toggleable.state = True
    assert toggleable._state


def test_getting_state():
    toggleable = Toggleable(enable, disable, True)
    toggleable.state = not toggleable.state
    assert not toggleable.state


def test_state_enable():
    state = State()
    Toggleable(lambda *_: state(True), lambda *_: state(False), True)
    assert state.state


def test_state_disable():
    state = State()
    Toggleable(lambda *_: state(True), lambda *_: state(False), False)
    assert not state.state
