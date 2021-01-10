

from typing import Optional, Dict
from pathlib import Path
from abc import abstractmethod

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin


class AbstractPluginLocator:
    """
    The class in charge of locating every plugin already installed
    """
    def __init__(self, destination_path: Optional[Path]):
        self.destination_path = destination_path
        self.plugins: Dict[str, AbstractPlugin] = self.find_all_plugins()

    @abstractmethod
    def find_all_plugins(self) -> Dict[str, AbstractPlugin]:
        """
        The actual function in charge of finding every valid function
        :return: a dictionary of the names of the plugin and the actual plugins themselves
        """

    @abstractmethod
    def validate_plugin(self, plugin: AbstractPlugin) -> bool:
        """
        Determines if a Plugin is a valid Plugin or not
        :return: if the Plugin is valid
        """