

import pytest

from foundry.plugins.Plugin.Plugin import Plugin
from foundry.plugins.Plugin.PluginFacade import PluginFacade
from foundry.plugins.Plugin.ActionPluginFacadeAdapter import ActionPluginFacadeAdapter

from foundry.core.Toggleable.UninitializedStateException import UninitializedStateException


def enable():
    return True


def disable():
    return False


def create():
    return 5


def destroy():
    return -5


class State:
    def __init__(self):
        self.state = None

    def __call__(self, state: bool) -> bool:
        self.state = state
        return True


def test_initialization():
    ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))


def test_uninitialized_state_exception():
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    with pytest.raises(UninitializedStateException):
        _ = toggleable.state


def test_setting_state():
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    toggleable.state = True
    assert toggleable.state
    assert toggleable._toggleable.state


def test_getting_state():
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    toggleable.state = True
    toggleable.state = not toggleable.state
    assert not toggleable.state


def test_state_enable():
    state = State()
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin(
        "name", create, destroy, lambda *_: state(True), lambda *_: state(False)
    )))
    toggleable.state = True
    assert state.state


def test_state_disable():
    state = State()
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin(
        "name", create, destroy, lambda *_: state(True), lambda *_: state(False)
    )))
    toggleable.state = False
    assert not state.state


def test_state_observer():
    state = State()
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    toggleable.state_update_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = True
    assert state.state
    toggleable.state = False
    assert not state.state


def test_enable_observer():
    state = State()
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    toggleable.enabled_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = True
    assert state.state


def test_disable_observer():
    state = State()
    toggleable = ActionPluginFacadeAdapter(PluginFacade(Plugin("name", create, destroy, enable, disable)))
    toggleable.disabled_action.observer.attach_observer(lambda value: state(value))
    toggleable.state = False
    assert not state.state
