

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
        self.observable_name = observable_name

    def __get__(self, instance, owner):
        self.create_observable(instance)
        func = partial(self.__call__, instance)
        return func

    def __call__(self, instance, *args, **kwargs):
        self.create_observable(instance)
        result = self.func(instance, *args, **kwargs)
        instance._observables[self.observable_name](result=result)
        return result

    def create_observable(self, instance):
        """
        Generates an observable for the instance of the class
        :return: an observable
        """
        if not hasattr(instance, "_observables"):
            instance._observables = {}
        if self.observable_name not in instance._observables:
            instance._observables.update({self.observable_name: Observable(name=self.observable_name)})


def observable_decorator(observable_name: str):
    """A decorator that attaches an ObservableDecorator to a method"""
    def decorator(function):
        """The actual decorator"""
        return ObservableDecorator(function, observable_name)
    return decorator
