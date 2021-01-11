

from pathlib import Path

from foundry.plugins.PluginLocator.PluginLocator import PluginLocator


def good_validator(*_):
    return True


def bad_validator(*_):
    return False


def plugin_finder(instance: PluginLocator):
    if instance.validator():
        return {"plugin": "not_a_plugin"}
    return {}


def test_initialization():
    PluginLocator(plugin_finder, good_validator, Path("test"))


def test_validator_success():
    plugin_locator = PluginLocator(plugin_finder, good_validator, Path("test"))
    assert len(plugin_locator.plugins) == 1

def test_validator_failure():
    plugin_locator = PluginLocator(plugin_finder, bad_validator, Path("test"))
    assert len(plugin_locator.plugins) == 0
