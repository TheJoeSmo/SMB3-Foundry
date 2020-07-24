"""
This module includes the SettingsMenuElement, which provides an interface to easily add boolean settings to the menu
SettingsMenuAction: The menu action in charge of settings
"""


from . import Menu, MenuAction
from foundry.gui.settings import set_setting, get_setting


class SettingsMenuAction(MenuAction):
    """Provides an easy interface to change settings from the Menu"""
    def __init__(self, parent: Menu, setting: str, name: str = "", add_action: bool = True) -> None:
        super(SettingsMenuAction, self).__init__(parent, get_setting(setting, True), name, add_action)
        self.add_observer(lambda value: set_setting(setting, value))