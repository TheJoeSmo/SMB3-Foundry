

from foundry.core.Action.Action import Action
from foundry.core.State.State import State
from foundry.core.Toggleable.ActionToggleable import ActionToggleable


class ActionToggleableFacadeSettingAdapter(State):
    """
    This class adapts a ToggleableFacade to act like a State
    """

    def __init__(self, name: str, toggleable: ActionToggleable):
        super().__init__(name, toggleable.state, Action)
        toggleable.enabled_action.observer.attach_observer(
            lambda *_: setattr(self, "state", True), f"{self} Toggleable Enabled"
        )
        toggleable.disabled_action.observer.attach_observer(
            lambda *_: setattr(self, "state", False), f"{self} Toggleable Disabled"
        )
        self.observer.attach_observer(
            lambda value: setattr(toggleable, "state", value)
        )
