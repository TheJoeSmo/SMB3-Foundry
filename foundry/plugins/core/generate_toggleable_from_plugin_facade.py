

from foundry.plugins.Plugin.PluginFacade import PluginFacade

from foundry.core.Toggleable.Toggleable import Toggleable


def generate_toggleable_from_plugin_facade(plugin: PluginFacade) -> Toggleable:
    """
    Generates a Toggleable from a given PluginFacade
    :param plugin: the PluginFacade
    :return: the Toggleable
    """
    return Toggleable(plugin.enable, plugin.disable)
