

from typing import Callable
from functools import update_wrapper, partial

from foundry.core.Observables.Observable import Observable


class ObservableDecorator:
    """
    A decorator that attaches an observer that updates every time the method is called.
    """
    def __init__(self, func: Callable, observable_name: str):
        update_wrapper(self, func)
        self.func = func
        self.observer = Observable(name=observable_name)

    def __get__(self, instance, owner):
        func = partial(self.__call__, instance)
        func.observer = self.observer  # make the observable visible through get
        return func

    def __call__(self, instance, *args, **kwargs):
        result = self.func(instance, *args, **kwargs)
        self.observer(result=result)
        return result


def observable_decorator(observable_name: str):
    """A decorator that attaches an ObservableDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return ObservableDecorator(function, observable_name)
    return decorator
