

from typing import Optional, Dict
from pathlib import Path
from abc import abstractmethod

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.PluginLocator import AbstractPluginLocator


class AbstractPluginCreator:
    """
    An interface for creating a plugin
    """

    def __init__(self, destination_path: Optional[Path], locator: AbstractPluginLocator):
        self.destination_path = destination_path
        self.plugins: Dict[str, AbstractPlugin] = locator.plugins

    def create_plugin(self, plugin: AbstractPlugin, plugin_path: Path) -> bool:
        """
        The method in charge of creating a plugin from start to finish.
        This method works by being passed an uninitialized Plugin and a directory to its data.
        As a FPL (ZIP) file is used to originally import the Plugin, it is suspected that the directory is in a temp
        location and will automatically handle deletion afterwards.
        :param plugin: The uninitialized Plugin in need of being created
        :param plugin_path: The path to the directory of any required data for the Plugin
        :return: if the Plugin was created
        """
        if not self.validate_plugin(plugin, plugin_path):
            return False
        self._create_plugin(plugin, plugin_path)
        return True

    @abstractmethod
    def validate_plugin(self, plugin, plugin_path: Path) -> bool:
        """
        Ensure the paths will not override any data
        :param plugin: The uninitialized Plugin in need of being created
        :param plugin_path: The path to the Plugin
        :return: if the Plugin is valid
        """

    @abstractmethod
    def _create_plugin(self, plugin: AbstractPlugin, plugin_path: Path):
        """
        The method in charge of actually handling the business logic of creating a Plugin
        :param plugin: The uninitialized Plugin in need of being created
        :param plugin_path: The path to the directory of any required data for the Plugin
        """
