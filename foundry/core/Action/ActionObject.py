

from typing import List
from inspect import getmembers, ismethoddescriptor

from foundry.core.Observables.Observable import Observable
from foundry.core.Action.Action import Action
from foundry.core.Action.AbstractActionObject import AbstractActionObject
from foundry.core.Action.util.smart_action_decorator import SmartActionDecorator


def get_all_smart_action_decorators(cls) -> List[SmartActionDecorator]:
    """
    Finds every class inside self and tests if it is a smart action decorator.
    :return: a list f SmartActionDecorators
    """
    return [member[1] for member in getmembers(cls, predicate=ismethoddescriptor)]


class ActionObject(AbstractActionObject):
    """
    A basic implementation of ActionObject that tests if each method inside the ActionObject has an observer and
    adds them automatically
    """

    def __init__(self) -> None:
        self._actions_enabled = {}
        super().__init__()

    def get_actions(self) -> List[Action]:
        """
        This method relies on the smart_action_decorator in order to work
        The method first finds every smart_action_decorator by testing if it has a create_action
        For each smart_action_decorator an Action will be created and appended to the list of actions that will
        be turned into the _actions that the ActionObject uses
        :return: a list of Actions
        """
        actions: List[Action] = []
        decorators = get_all_smart_action_decorators(self)
        for decorator in decorators:
            try:
                actions.append(Action(name=decorator.action_name, observer=Observable(name=decorator.observable_name)))
                self._actions_enabled[decorator.action_name] = True
            except AttributeError:
                continue
        return actions



