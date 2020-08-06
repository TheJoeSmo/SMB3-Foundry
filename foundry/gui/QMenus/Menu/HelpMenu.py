from foundry.gui.QMenus.HelpMenu import FeatureVideoMenuElement, GitMenuElement, \
    DiscordMenuElement, AboutMenuElement
from foundry.gui.QMenus.MenuElement.MenuElementCheckForUpdate import MenuElementCheckForUpdate
from foundry.gui.QMenus.Menu.Menu import Menu


class HelpMenu(Menu):
    """A menu for providing help"""
    def __init__(self, parent):
        super().__init__(parent, "Help")
        self.parent = parent

        self.updater_action = MenuElementCheckForUpdate(self.parent, False)
        self.add_action(self.updater_action.name, self.updater_action.action)
        self.addSeparator()
        self.feature_video_action = FeatureVideoMenuElement(self)
        self.git_action = GitMenuElement(self)
        self.discord_action = DiscordMenuElement(self)
        self.about_action = AboutMenuElement(self.parent, False)
        self.addSeparator()
        self.add_action(self.about_action.name, self.about_action.action)