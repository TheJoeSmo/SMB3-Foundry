

import pytest

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException
from foundry.core.Toggleable.ObservableToggleable import ObservableToggleable
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
    ObservableToggleable(Toggleable(enable, disable))


def test_uninitialized_state_exception():
    toggleable = ObservableToggleable(Toggleable(enable, disable))
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state_from_init():
    toggleable = ObservableToggleable(Toggleable(enable, disable, True))
    assert toggleable._toggleable.state


def test_setting_state():
    toggleable = ObservableToggleable(Toggleable(enable, disable))
    toggleable.state = True
    assert toggleable.state
    assert toggleable._toggleable.state


def test_getting_state():
    toggleable = ObservableToggleable(Toggleable(enable, disable, True))
    toggleable.state = not toggleable.state
    assert not toggleable.state


def test_state_enable():
    state = State()
    ObservableToggleable(Toggleable(lambda *_: state(True), lambda *_: state(False), True))
    assert state.state


def test_state_disable():
    state = State()
    ObservableToggleable(Toggleable(lambda *_: state(True), lambda *_: state(False), False))
    assert not state.state


def test_state_observer():
    state = State()
    toggleable = ObservableToggleable(Toggleable(enable, disable))
    toggleable.state_update_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = True
    assert state.state
    toggleable.state = False
    assert not state.state


def test_enable_observer():
    state = State()
    toggleable = ObservableToggleable(Toggleable(enable, disable))
    toggleable.enabled_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = True
    assert state.state


def test_disable_observer():
    state = State()
    toggleable = ObservableToggleable(Toggleable(enable, disable))
    toggleable.disabled_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = False
    assert not state.state
