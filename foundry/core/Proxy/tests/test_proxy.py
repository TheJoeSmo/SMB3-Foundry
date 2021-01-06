

from foundry.core.Proxy.Proxy import Proxy


class TestClass:
    """Just a class with some basic functionality"""
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    def method(self, value) -> None:
        return value + 1


def test_initialization():
    Proxy(TestClass(0))


def test_getting_value():
    proxy = Proxy(TestClass(12))
    assert proxy.value == 12


def test_setting_value():
    proxy = Proxy(TestClass(12))
    proxy.value = 13
    assert proxy.value == 13


def test_calling_method():
    proxy = Proxy(TestClass(0))
    assert proxy.method(0) == 1
