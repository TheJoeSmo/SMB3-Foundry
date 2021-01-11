

from pathlib import Path

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.PluginCreator.PluginCreator import PluginCreator


def plugin_validator(creator: PluginCreator, plugin: AbstractPlugin, plugin_path: Path) -> bool:
    """
    A simple validator for a plugin
    The validator ensures that the plugin name matches is not already created inside the path
    The validator also ensures that it is not already inside the creator
    :param creator: The PluginCreator with the already known plugins created
    :param plugin: The uninitialized Plugin in need of being created
    :param plugin_path: The path to the Plugin
    :return: if the plugin is valid or not
    """
    plugin_name = plugin.name
    plugin_directory = creator.destination_path / plugin_name
    if plugin_directory.is_file():
        return False  # Plugin name conflicts PluginCreator directory
    if plugin_name in creator.plugins:
        return False  # Plugin was already created
    return True

