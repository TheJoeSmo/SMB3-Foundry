

from foundry.plugins.Plugin.Plugin import Plugin


def enable():
    return True

def disable():
    return False

def create():
    return 1000

def delete():
    return -1000


def test_initialization():
    Plugin("test", create, delete, enable, disable)


def test_create():
    plugin = Plugin("test", create, delete, enable, disable)
    assert plugin.create() == 1000


def test_delete():
    plugin = Plugin("test", create, delete, enable, disable)
    assert plugin.delete() == -1000


def test_enable():
    plugin = Plugin("test", create, delete, enable, disable)
    assert plugin.enable()


def test_disable():
    plugin = Plugin("test", create, delete, enable, disable)
    assert not plugin.disable()
