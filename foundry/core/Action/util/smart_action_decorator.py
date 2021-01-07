

from typing import Callable
from functools import partial

from foundry.core.Action.util.action_decorator import ActionDecorator as ActionDecorator


class SmartActionDecorator(ActionDecorator):
    """
    A action decorator that is identifiable until it is initialized
    """

    def __init__(self, func: Callable, action_name: str, observable_name: str):
        super().__init__(func, action_name, observable_name)

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
        instance._actions[self.action_name](result=result)
        return result

    def create_action(self, instance):
        instance._actions_enabled[self.action_name] = True
        super().create_action(instance)


def smart_action_decorator(action_name: str, observable_name: str):
    """A decorator that attaches an ActionDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return SmartActionDecorator(function, action_name, observable_name)
    return decorator
