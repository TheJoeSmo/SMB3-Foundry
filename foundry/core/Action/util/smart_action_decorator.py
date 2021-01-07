

from typing import Callable
from functools import partial

from foundry.core.Observables.Observable import Observable
from foundry.core.Action.Action import Action
from foundry.core.Action.util.action_decorator import ActionDecorator as ActionDecorator


class SmartActionDecorator(ActionDecorator):
    """
    A action decorator that is identifiable until it is initialized
    """

    def __init__(self, func: Callable, action_name: str, observable_name: str):
        super().__init__(func, action_name, observable_name)
        self.reference_name = f"{action_name}_action"

    def __get__(self, instance, owner):
        if not hasattr(instance, "_actions_enabled"):
            instance._actions_enabled = {}
        if self.action_name not in instance._actions_enabled:
            instance._actions_enabled.update({self.action_name: False})

        if not instance._actions_enabled[self.action_name]:
            return self
        else:
            return partial(self.__call__, instance)

    def __call__(self, instance, *args, **kwargs):
        result = self.func(instance, *args, **kwargs)
        instance._actions[self.reference_name](result=result)
        return result

    def create_action(self, instance):
        instance._actions_enabled[self.action_name] = True
        if not hasattr(instance, "_actions"):
            instance._actions = {}
        if self.action_name not in instance._actions:
            observer = Observable(name=self.observable_name)
            self.action = Action(name=self.action_name, observer=observer)
            instance._actions.update({self.reference_name: self.action})


def smart_action_decorator(action_name: str, observable_name: str):
    """A decorator that attaches an ActionDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return SmartActionDecorator(function, action_name, observable_name)
    return decorator
