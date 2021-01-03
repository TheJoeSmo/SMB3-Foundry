

from shutil import move
from os import mkdir
from typing import Optional
from pathlib import Path

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin
from foundry.plugins.core.PluginDirectoryNameException import PluginDirectoryNameException


def load_plugin(plugin: AbstractPlugin, external_path: Optional[Path], destination_path: Optional[Path]) -> None:
    """
    This function does the job of moving an external directory inside the project in order to provide any additional
    files or Plugins required for the Plugin to work properly.
    This function makes the assumption that the original Plugin was already installed, as it had to run in order to
    call this function.  Thus, the only job of load_plugin is simply moving the directory from a given spot to inside
    the plugin directory.

    The function also requires the name of the directory to match with the actual Plugin name.  If the name does not
    match, it will raise a PluginDirectoryNameException in order to prevent any corruption or overriding.
    :param plugin: The Plugin that is trying to import its directory.
    :param external_path: The path to directory that the Plugin is trying to import.
    :param destination_path: The path to directory that the Plugin is trying export to.
    """
    if external_path.name != plugin.name:
        raise PluginDirectoryNameException(str(external_path), plugin.name)

    destination_path = destination_path.joinpath(plugin.name)
    mkdir(str(destination_path))

    move(str(external_path), str(destination_path))
