

from typing import Callable
from functools import update_wrapper, partial

from foundry.core.Observables.Observable import Observable
from foundry.core.Action.Action import Action


class ActionDecorator:
    """
    A decorator that attaches an action that updates every time the method is called.
    """
    def __init__(self, func: Callable, action_name: str, observable_name: str):
        update_wrapper(self, func)
        self.func = func
        self.observable_name = observable_name
        self.action_name = action_name
        self.action = None

    def __get__(self, instance, owner):
        self.create_action(instance)
        func = partial(self.__call__, instance)
        return func

    def __call__(self, instance, *args, **kwargs):
        self.create_action(instance)
        result = self.func(instance, *args, **kwargs)
        instance._actions[self.action_name](result=result)
        return result

    def create_action(self, instance):
        """
        Generates an action for the instance of the class
        :return: an action
        """
        if not hasattr(instance, "_actions"):
            instance._actions = {}
        if self.action_name not in instance._actions:
            observer = Observable(name=self.observable_name)
            self.action = Action(name=self.action_name, observer=observer)
            instance._actions.update({self.action_name: self.action})


def action_decorator(action_name: str, observable_name: str):
    """A decorator that attaches an ActionDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return ActionDecorator(function, action_name, observable_name)
    return decorator
