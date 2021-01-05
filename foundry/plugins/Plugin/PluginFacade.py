

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin


class PluginFacade:
    """
    Simplifies the API to just the enable and disable functions.
    """

    def __init__(self, plugin: AbstractPlugin) -> None:
        self._plugin = plugin

    def enable(self) -> bool:
        """
        Enables itself and handles any other requirements that are needed
        :return: a bool depending if it enabled itself successfully
        """
        return self._plugin.enable()

    def disable(self) -> bool:
        """
        Disable itself and handles any other disabling required
        :return: a bool depending if it disabled itself successfully
        """
        return self._plugin.disable()
