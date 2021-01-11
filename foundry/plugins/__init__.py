

from typing import Dict, Set, FrozenSet
from pathlib import Path
from os import listdir
from os.path import isfile, join, splitext
import importlib

from foundry.core.Observables.ObservableDecorator import ObservableDecorator
from foundry.core.Action.Action import Action
from foundry.core.Settings.SettingsContainer import SettingsContainer
from foundry.core.Settings.Setting import Setting
from foundry.core.util import default_settings_dir
from foundry import data_dir

plugins_setting_dir = default_settings_dir / "file_name" / "plugins"
plugins_setting_dir.mkdir(parents=True, exist_ok=True)
plugins_container = SettingsContainer.from_json_file("plugins", plugins_setting_dir, True)

plugins_dir = data_dir / "foundry" / "plugins" / "plugins"
