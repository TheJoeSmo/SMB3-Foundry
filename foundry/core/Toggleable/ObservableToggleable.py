

from foundry.core.Toggleable.AbstractToggleable import AbstractToggleable
from foundry.core.Action.API.ActionObject import ActionObject, action_decorator
from foundry.core.Action.Action import Action


class ObservableToggleable(ActionObject, AbstractToggleable):
    """
    A toggleable object that emits updates everytime it is toggled
    """
    enabled_action: Action
    disabled_action: Action
    state_update_action: Action

    def __init__(self, toggleable: AbstractToggleable, **kwargs):
        self._toggleable = toggleable
        super().__init__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._toggleable})"

    @property
    def state(self) -> bool:
        return self._toggleable.state

    @state.setter
    def state(self, state: bool) -> None:
        self._set_state(state)
        self.enable() if self.state else self.disable()

    @action_decorator("state_update", "state_update")
    def _set_state(self, state: bool) -> bool:
        self._toggleable.state = state
        return state

    @action_decorator("enabled", "enabled")
    def enable(self, *args, **kwargs) -> bool:
        return self._toggleable.enable(*args, **kwargs)

    @action_decorator("disabled", "disabled")
    def disable(self, *args, **kwargs) -> bool:
        return self._toggleable.disable(*args, **kwargs)
