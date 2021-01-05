

from typing import Callable, Dict

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.Plugin.Plugin import Plugin
from foundry.plugins.PluginManager.AbstractPluginManager import AbstractPluginManager


class PluginManager(Plugin, AbstractPluginManager):
    """
    A generic implementation of a PluginManager.
    This PluginManager implements a real world way to instantiate plugins in a real context.
    """

    def __init__(
            self,
            name: str,
            create: Callable,
            delete: Callable,
            enable: Callable,
            disable: Callable,
            handler: Callable,
            plugins: Dict[AbstractPlugin, bool],
            create_plugin: Callable,
            delete_plugin: Callable,
            enable_plugin: Callable,
            disable_plugin: Callable,
            **kwargs
    ) -> None:
        super().__init__(
            name=name,
            create=create,
            delete=delete,
            enable=enable,
            disable=disable,
            handler=handler,
            plugins=plugins
        )
        self._create_plugin = create_plugin
        self._delete_plugin = delete_plugin
        self._enable_plugin = enable_plugin
        self._disable_plugin = disable_plugin

    def create_plugin(self, plugin: AbstractPlugin) -> bool:
        return self._create_plugin(plugin)

    def delete_plugin(self, plugin: AbstractPlugin) -> bool:
        return self._delete_plugin(plugin)

    def enable_plugin(self, plugin: AbstractPlugin) -> bool:
        return self._enable_plugin(plugin)

    def disable_plugin(self, plugin: AbstractPlugin) -> bool:
        return self._disable_plugin(plugin)
