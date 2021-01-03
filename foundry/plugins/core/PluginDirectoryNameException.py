

class PluginDirectoryNameException(Exception):
    """
    This exception is called whenever an invalid directory is tried to be installed by a Plugin.

    An invalid directory is any directory which name is not identical to its Plugin name.  The purpose of this
    exception is to limit an external Plugin from corrupting or overriding another Plugin.  This allows for a
    Plugin to be limited to a single directory that is the same name as itself
    """
    def __init__(self, directory: str, name: str):
        super().__init__(f"Invalid directory {directory} name, must be identical to {name}")
