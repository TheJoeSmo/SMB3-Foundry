

from abc import abstractmethod

from foundry.plugins.Plugin.AbstractPlugin import AbstractPlugin


class AbstractPluginHandler:
    """
    This is an interface of what a PluginHandler should do.
    The purpose of a PluginHandler is to connect an implementation of AbstractPlugin to simpler interface.
    A PluginHandler implements a toggleable enabled property that can be used to control the state of the injected
    AbstractPlugin.  Furthermore, a PluginHandler assumes that the AbstractPlugin is already created and hides those
    implementations to ensure that the AbstractPlugin cannot be accidentally destroyed.
    """

    def __init__(self, plugin: AbstractPlugin, value: bool) -> None:
        self._plugin = plugin
        self.enabled = value

    def toggle(self) -> None:
        """Toggles the value of the PluginHandler"""
        self.enabled = not self.enabled

    @property
    @abstractmethod
    def enabled(self) -> bool:
        """
        The status of the AbstractPlugin being enabled or disabled
        :return: if the AbstractPlugin is enabled
        """

    @enabled.setter
    @abstractmethod
    def enabled(self, enabled: bool) -> None:
        """
        Enables or disables the AbstractPlugin and provides any required updates
        :param enabled: Sets the if the AbstractPlugin should be enabled or disabled
        """
