

from foundry.plugins.core.generate_toggleable_from_plugin_facade import generate_toggleable_from_plugin_facade
from foundry.plugins.Plugin.PluginFacade import PluginFacade

from foundry.core.Toggleable.ActionToggleable import ActionToggleable


class ActionPluginFacadeAdapter(ActionToggleable):
    """
    This class adapts a PluginFacade into a Toggleable that adheres to the observable system
    """

    def __init__(self, plugin: PluginFacade, **kwargs):
        super().__init__(generate_toggleable_from_plugin_facade(plugin))
