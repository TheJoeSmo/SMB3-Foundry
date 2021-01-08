

from pytest import raises

from foundry.plugins.Plugin.Plugin import Plugin
from foundry.plugins.Plugin.PluginFacade import PluginFacade


def enable():
    return True

def disable():
    return False

def create():
    return 1000

def delete():
    return -1000


def test_initialization():
    PluginFacade(Plugin("test", create, delete, enable, disable))


def test_create():
    plugin = PluginFacade(Plugin("test", create, delete, enable, disable))
    with raises(AttributeError):
        plugin.create()


def test_delete():
    plugin = PluginFacade(Plugin("test", create, delete, enable, disable))
    with raises(AttributeError):
        plugin.delete()


def test_enable():
    plugin = PluginFacade(Plugin("test", create, delete, enable, disable))
    assert plugin.enable()


def test_disable():
    plugin = PluginFacade(Plugin("test", create, delete, enable, disable))
    assert not plugin.disable()
