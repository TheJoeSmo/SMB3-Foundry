"""
An very simple integration test to verify that an ActionObject can find every action_decorator and add those
automatically to the class automatically
"""

from foundry.core.Action.Action import Action
from foundry.core.Action.ActionObject import ActionObject
from foundry.core.Action.util.smart_action_decorator import smart_action_decorator as action_decorator


class Test(ActionObject):
    method_action: Action

    @action_decorator("method", "method")
    def method(self) -> int:
        return 5


def test_initialization():
    Test()


def test_getting_method():
    test = Test()
    assert len(test._actions) == 1
