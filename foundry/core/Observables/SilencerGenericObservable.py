

from foundry.core.Silencer.Silencer import Silencer
from foundry.core.Observables.Observable import Observable
from foundry.core.Observables.core.attach_observer import attach_observer
from foundry.core.Observables.core.notify_observers import notify_observers
from foundry.core.Observables.core.delete_observer import delete_observer


class SilencerGenericObservable(Observable):
    """
    An observable with the ability to silence notifications from occurring
    """

    def __init__(self, name: str, silenced: bool = False):
        self.silencer = Silencer(notify_observers, silenced)
        super().__init__(self.silencer, attach_observer, delete_observer, name)

    @property
    def silenced(self) -> bool:
        """If the observable is silenced"""
        return self.silencer.silenced

    @silenced.setter
    def silenced(self, silenced: bool) -> None:
        self.silencer.silenced = silenced
