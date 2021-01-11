

from pathlib import Path

from foundry.plugins.core.plugin_validator import plugin_validator
from foundry.plugins.Plugin.Plugin import Plugin


class FakeCreator:
    def __init__(self, plugins):
        self.plugins = plugins
        self.destination_path = Path()


def test_valid_file(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda *_: False)
    plugin = Plugin("test", lambda *_: True, lambda *_: True, lambda *_: True, lambda *_: True)
    creator = FakeCreator({})
    assert plugin_validator(creator, plugin, "not_a_path")


def test_invalid_file(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda *_: True)
    plugin = Plugin("test", lambda *_: True, lambda *_: True, lambda *_: True, lambda *_: True)
    creator = FakeCreator({})
    assert not plugin_validator(creator, plugin, "not_a_path")


def test_inside_plugins():
    plugin = Plugin("test", lambda *_: True, lambda *_: True, lambda *_: True, lambda *_: True)
    creator = FakeCreator({"test", plugin})
    assert not plugin_validator(creator, plugin, "not_a_path")


def test_not_inside_plugins():
    plugin = Plugin("test", lambda *_: True, lambda *_: True, lambda *_: True, lambda *_: True)
    creator = FakeCreator({"not_test", plugin})
    assert plugin_validator(creator, plugin, "not_a_path")
