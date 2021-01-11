

from pathlib import Path

from foundry.plugins.PluginCreator.PluginCreator import PluginCreator


def good_validator(*_):
    return True


def bad_validator(*_):
    return False


def create_plugin(*_):
    pass


class FakeLocator():
    def __init__(self):
        self.plugins = {}


def test_initialization():
    PluginCreator(good_validator, create_plugin, Path("test"), FakeLocator())


def test_validator_success():
    plugin_creator = PluginCreator(good_validator, create_plugin, Path("test"), FakeLocator())
    fake_plugin = FakeLocator()
    fake_plugin.name = "totally_a_name"
    assert plugin_creator.create_plugin(fake_plugin, Path("test"))


def test_validator_failure():
    plugin_creator = PluginCreator(bad_validator, create_plugin, Path("test"), FakeLocator())
    assert not plugin_creator.create_plugin("not_a_plugin", Path("test"))
