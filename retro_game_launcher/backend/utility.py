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

def environment_map(**variables) -> dict[str, str | list[str]]:
    """
    Create an environment map.

    Returns:
        dict[str, str | list[str]]: A dictionary of variable names with a key.
    """
    env = {
        'XDG_CONFIG_HOME': GLib.get_user_config_dir(),
        'XDG_DATA_HOME': GLib.get_user_data_dir(),
        'CONFIG_DIR': user_config_directory(),
        'DATA_DIR': user_data_directory(),
    }
    for key, value in variables.items():
        env[key] = value
    return env

def environment_replace_command(command: list[str], **variables) -> list[str]:
    """
    Replace all variables in a command with the appropriate substitutions.

    Parameters:
        command (list[str]): The source command.

    Returns:
        list[str]: The output command.
    """
    replaced = command.copy()
    items = variables.items()
    has_key = True
    while has_key:
        has_key = False
        for key, value in items:
            env = '${%s}' % key
            if value is not None and env in replaced:
                has_key = True
                index = replaced.index(env)
                if key.startswith('CMD_'):
                    replaced.remove(env)
                    for i in range(len(value)):
                        replaced.insert(index + i, value[i])
                else:
                    replaced[index] = value
    return replaced
