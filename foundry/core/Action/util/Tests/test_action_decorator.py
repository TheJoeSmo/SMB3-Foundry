

import pytest

from foundry.core.Action.util.action_decorator import action_decorator
from foundry.core.Action.Action import Action


class TestClass:
    def __init__(self):
        self.value = 0
        self.add_one()
        self.add_value(-1)  # initialize the actions

    @action_decorator("add_one", "add_one")
    def add_one(self) -> int:
        self.value += 1
        return self.value

    @action_decorator("add_value", "add_value")
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


def test_action():
    test, copy = TestClass(), TestClass()
    action: Action = test._actions["add_one"]
    action.observer.attach_observer(lambda value: setattr(copy, "value", value))
    test.add_one()
    assert copy.value == 1
    test.add_value(5)
    assert copy.value == 1
    test.add_one()
    assert copy.value == 7


def test_action_for_each_instance():
    test_one, test_two, copy = TestClass(), TestClass(), TestClass()
    action: Action = test_one._actions["add_one"]
    action.observer.attach_observer(lambda value: setattr(copy, "value", value))
    test_one.add_one()
    test_two.add_value(5)
    test_two.add_one()
    assert copy.value == 1
