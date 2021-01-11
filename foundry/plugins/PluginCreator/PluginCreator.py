

from typing import Optional, Callable
from pathlib import Path

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.PluginLocator.AbstractPluginLocator import AbstractPluginLocator
from foundry.plugins.PluginCreator.AbstractPluginCreator import AbstractPluginCreator


class PluginCreator(AbstractPluginCreator):
    """
    A basic implementation of a PluginCreator that uses dependency injection
    """

    def __init__(
            self,
            validator: Callable,
            creator: Callable,
            destination_path: Optional[Path],
            locator: AbstractPluginLocator):
        self.validator = validator
        self.creator = creator
        super().__init__(destination_path, locator)

    def validate_plugin(self, plugin_path: Path) -> bool:
        """
        Ensure the paths will not override any data
        :param plugin_path: The path to the Plugin
        :return: if the Plugin is valid
        """
        return self.validator(self, plugin_path)

    def _create_plugin(self, plugin: AbstractPlugin, plugin_path: Path):
        """
        The method in charge of actually handling the business logic of creating a Plugin
        :param plugin: The uninitialized Plugin in need of being created
        :param plugin_path: The path to the directory of any required data for the Plugin
        """
        self.creator(self, plugin, plugin_path)
        self.plugins.update({plugin.name: plugin})
