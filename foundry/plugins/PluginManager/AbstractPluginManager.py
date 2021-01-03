

from typing import Dict, Callable
from abc import ABC, abstractmethod

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin


class AbstractPluginManager(AbstractPlugin, ABC):
    """
    This is an interface of what a PluginManager should do.
    The purpose of a PluginManager is two fold.  A PluginManager is simply multiple Plugins.  In the same token,
    multiple Plugins is ultimately a Plugin.  The main advantage of using a PluginManager, is it denoting an official
    boarder from which external commands must go through it and from which internal commands must stay inside.
    This allows for a Plugin to continue to generate Plugins for itself while isolating each and every Plugin into its
    own unit that can be tested and replaced with relative ease.
    """

    def __init__(self, name: str, handler: Callable, plugins: Dict[AbstractPlugin, bool]) -> None:
        """
        Creates a series of plugins that cna be handled
        :param handler: An implementation of AbstractPluginHandler to be used to generate
        :param plugins:
        """
        super().__init__(name)
        self._handler = handler
        self.plugins = [handler(plugin, enabled) for plugin, enabled in plugins.items()]

    @abstractmethod
    def create_plugin(self, plugin: AbstractPlugin) -> None:
        """
        Initializes the Plugin and converts it to a PluginHandler for later use
        :param plugin: A Plugin that has not been created yet
        """

    @abstractmethod
    def delete_plugin(self, plugin: AbstractPlugin) -> None:
        """
        Destroys the Plugin and cleans up anything needed
        :param plugin: A Plugin that will be destroyed
        """

    @abstractmethod
    def enable_plugin(self, plugin: AbstractPlugin):
        """
        Enables a Plugin and does any additional requirements
        :param plugin: A Plugin that will be enabled
        """

    @abstractmethod
    def disable_plugin(self, plugin: AbstractPlugin):
        """
        Disables a Plugin and does any additional requirements
        :param plugin: A Plugin that will be disabled
        """
