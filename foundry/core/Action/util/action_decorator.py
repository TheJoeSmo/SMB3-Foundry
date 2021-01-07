

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
        observer = Observable(name=observable_name)
        self.action = Action(name=action_name, observer=observer)

    def __get__(self, instance, owner):
        func = partial(self.__call__, instance)
        func.action = self.action  # make the observable visible through get
        return func

    def __call__(self, instance, *args, **kwargs):
        result = self.func(instance, *args, **kwargs)
        self.action(result=result)
        return result


def action_decorator(action_name: str, observable_name: str):
    """A decorator that attaches an ActionDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return ActionDecorator(function, action_name, observable_name)
    return decorator
