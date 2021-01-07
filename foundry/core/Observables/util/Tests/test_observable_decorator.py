

import pytest

from foundry.core.Observables.util.observable_decorator import observable_decorator
from foundry.core.Observables.AbstractObservable import AbstractObservable


class TestClass:
    def __init__(self):
        self.value = 0
        self.add_one()
        self.add_value(-1)  # Set up the observers for the class

    @observable_decorator("add_one")
    def add_one(self) -> int:
        self.value += 1
        return self.value

    @observable_decorator("add_value")
    def add_value(self, value: int = 1) -> int:
        self.value += value
        return self.value


def test_initialization():
    TestClass()


def test_simple_method_call():
    test = TestClass()
    assert test.add_one() == 1
    assert test.value == 1


def test_complex_method_call():
    test = TestClass()
    assert test.add_value(5) == 5
    assert test.value == 5


def test_observer():
    test, copy = TestClass(), TestClass()
    observer: AbstractObservable = test._observables["add_one"]
    observer.attach_observer(lambda value: setattr(copy, "value", value))
    test.add_one()
    assert copy.value == 1
    test.add_value(5)
    assert copy.value == 1
    test.add_one()
    assert copy.value == 7


def test_observer_for_each_instance():
    test_one, test_two, copy = TestClass(), TestClass(), TestClass()
    observer: AbstractObservable = test_one._observables["add_one"]
    observer.attach_observer(lambda value: setattr(copy, "value", value))
    test_one.add_one()
    test_two.add_value(5)
    test_two.add_one()
    assert copy.value == 1
