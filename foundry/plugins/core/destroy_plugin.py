

from pathlib import Path
from shutil import rmtree


def destroy_plugin(plugin_path: Path) -> bool:
    """
    Destroys the plugin inputted
    :param plugin_path: The path of the Plugin to be destroyed
    :return: if successful
    """
    rmtree(plugin_path)
    return True
