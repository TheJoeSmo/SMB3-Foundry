

from pathlib import Path
from os import listdir, path
from shutil import move

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.PluginCreator.AbstractPluginCreator import AbstractPluginCreator


def create_plugin(creator: AbstractPluginCreator, plugin: AbstractPlugin, plugin_path: Path):
    """
    The function actually in charge of creating the plugin in the correct spot in memory
    This function takes a directory called plugin_path and moves it to the PluginCreator's directory
    :param creator: The PluginCreator that will supply the directory to move the plugin into
    :param plugin: The Plugin that will be set into the
    :param plugin_path: The path to the Plugin's data
    """
    plugin_directory = creator.destination_path / plugin.name
    plugin_directory.mkdir()

    for file in listdir(plugin_path):
        move(path.join(plugin_path, file), plugin_directory)

