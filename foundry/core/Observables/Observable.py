"""
This module includes Observable
This serves as a generic implementation of the AbstractObserver
"""

import random
from inspect import signature
from typing import Callable, Any, Dict, Optional, Hashable

from .AbstractObservable import AbstractObservable
from ..logs.observables import logger


class Observable(AbstractObservable):
    """
    A generic implementation of the AbstractObservable
    observables: A group of callables that will be notified of the result
    notify_observers: Notifies the observables
    attach_observer: Adds a callable to the dict of observables
    delete_observer: Removes a callable to the dict of observables
    """
    observers: Dict

    def __init__(self, name: str = None):
        super(Observable, self).__init__(name)

    def notify_observers(self, result: Any) -> None:
        """Update all the observers"""
        if len(self.observers) > 0:  # Ignore observers that do nothing
            try:
                logger.debug(
                    f"{str(self)} notified {[obs.__observer_name for obs in self.observers.values()]} result {result}"
                )
            except AttributeError:
                logger.debug(
                    f"{str(self)} notified {[obs.__class__.__name__ for obs in self.observers.values()]} result {result}"
                )
        keys_to_remove = []
        for key, observer in self.observers.items():
            try:
                observer(result)
            except NameError:
                keys_to_remove.append(key)  # the observer no longer exists
            except TypeError as err:
                logger.error(f"{err}: {observer.__class__.__name__}{str(signature(observer))} received {result}")
                raise TypeError(f"{observer.__class__.__name__}{str(signature(observer))} received {result}")

        for key in keys_to_remove:
            #  remove any observer that no longer exists
            self.delete_observable(key)

    def attach_observer(self, observer: Callable, identifier: Hashable = None, name: str = None) -> None:
        """Attach an observer"""
        while identifier is None:
            temp_id = random.randint(10000, 10000000)
            if temp_id not in self.observers:
                identifier = temp_id
        if name is not None:
            try:
                observer.__observer_name = name  # Tag the event for debugging
            except AttributeError as e:
                logger.warning(f"{e}: {self.name} failed to name {observer} the name {name}")
        self.observers.update({identifier: observer})

    def delete_observable(self, identifier: Hashable) -> None:
        """Removes an observer"""
        try:
            del self.observers[identifier]
        except KeyError:
            logger.warning(f"Failed to delete {identifier} from {self.observers}")
