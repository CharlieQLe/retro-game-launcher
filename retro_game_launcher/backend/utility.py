import os
import gi
from gi.repository import Gio, GLib
from retro_game_launcher.backend import constants

def user_config_directory() -> str:
    """
    Get the directory for this project's configs.

    Returns:
        str: The path to the config directory.
    """
    return os.path.join(GLib.get_user_config_dir(), constants.app_name)

def user_data_directory() -> str:
    """
    Get the directory for this project's data.

    Returns:
        str: The path to the data directory.
    """
    return os.path.join(GLib.get_user_data_dir(), constants.app_name)

def system_data_dirs() -> list[str]:
    return list(map(lambda dir : os.path.join(dir, constants.app_name), GLib.get_system_data_dirs()))

def get_presets() -> list[str]:
    presets = []
    for dir in filter(lambda dir : os.path.isdir(dir), map(lambda dir : os.path.join(dir, 'presets'), system_data_dirs())):
        presets.extend(list(map(lambda f : os.path.join(dir, f), filter(lambda f : not os.path.isdir(f) and f.endswith('.json'), os.listdir(dir)))))
    return presets
