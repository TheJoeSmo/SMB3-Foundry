

from foundry.core.Toggleable.AbstractToggleable import AbstractToggleable


class ToggleableFacade:
    """
    A class to generate a simpler API for a Toggleable just consisting of the state
    """

    def __init__(self, toggleable: AbstractToggleable, *_, **__) -> None:
        self._toggleable = toggleable

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._toggleable})"

    @property
    def state(self) -> bool:
        """The state of the plugin"""
        return self._toggleable.state

    @state.setter
    def state(self, state: bool) -> None:
        self._toggleable.state = state
