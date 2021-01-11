

from typing import Optional, Dict, Callable
from pathlib import Path

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin

from foundry.plugins.PluginLocator.AbstractPluginLocator import AbstractPluginLocator


class PluginLocator(AbstractPluginLocator):
    """
    A basic implementation of a PluginLocator using dependency injection
    """

    def __init__(self, finder: Callable, validator: Callable, destination_path: Optional[Path]):
        self.finder = finder
        self.validator = validator
        super().__init__(destination_path)

    def find_all_plugins(self) -> Dict[str, AbstractPlugin]:
        """
        The actual function in charge of finding every valid function
        :return: a dictionary of the names of the plugin and the actual plugins themselves
        """
        return self.finder(self)

    def validate_plugin(self, plugin: AbstractPlugin) -> bool:
        """
        Determines if a Plugin is a valid Plugin or not
        :return: if the Plugin is valid
        """
        return self.validator(self, plugin)
