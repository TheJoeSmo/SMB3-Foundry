

from shutil import rmtree
from filecmp import dircmp

from foundry import root_dir
from foundry.plugins.core.create_plugin import create_plugin

plugin_dir = root_dir / "foundry" / "plugins" / "core" / "tests" / "test_directory"
destination_dir = root_dir / "foundry" / "plugins" / "core" / "tests" / "destination"
final_dir = root_dir / "foundry" / "plugins" / "core" / "tests" / "destination" / "test"


class FakeCreator:
    def __init__(self):
        self.destination_path = destination_dir


class FakePlugin:
    def __init__(self):
        self.name = "test"


def test_create_plugin():
    rmtree(final_dir)  # We get an error if we already created the directory, so remove it

    create_plugin(FakeCreator(), FakePlugin(), plugin_dir)

    assert dircmp(plugin_dir, final_dir)
