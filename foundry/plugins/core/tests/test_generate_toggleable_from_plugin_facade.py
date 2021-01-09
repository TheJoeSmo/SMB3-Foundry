

from foundry.plugins.Plugin.Plugin import Plugin
from foundry.plugins.Plugin.PluginFacade import PluginFacade

from foundry.plugins.core.generate_toggleable_from_plugin_facade import generate_toggleable_from_plugin_facade


def enable():
    return True


def disable():
    return False


def create():
    return 5


def destroy():
    return -5


def test_initializations():
    generate_toggleable_from_plugin_facade(PluginFacade(Plugin("", create, destroy, enable, disable)))


def test_enable():
    toggleable = generate_toggleable_from_plugin_facade(PluginFacade(Plugin("", create, destroy, enable, disable)))
    assert toggleable.enable() == enable()


def test_disable():
    toggleable = generate_toggleable_from_plugin_facade(PluginFacade(Plugin("", create, destroy, enable, disable)))
    assert toggleable.disable() == disable()
