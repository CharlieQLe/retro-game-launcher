import os
import gi
from gi.repository import Gio
from retro_game_launcher.backend import constants

def user_config_directory() -> str:
    """
    Get the directory for this project's configs.

    Returns:
        str: The path to the config directory.
    """
    xdg_config_home = os.getenv('XDG_CONFIG_HOME')
    if not xdg_config_home:
        xdg_config_home = os.path.join(os.getenv('HOME'), '.config')
    return os.path.join(xdg_config_home, constants.app_name)

def user_data_directory() -> str:
    """
    Get the directory for this project's data.

    Returns:
        str: The path to the data directory.
    """
    xdg_data_home = os.getenv('XDG_DATA_HOME')
    if not xdg_data_home:
        xdg_data_home = os.path.join(os.getenv('HOME'), '.local', 'share')
    return os.path.join(xdg_data_home, constants.app_name)

def environment_map(**kwargs) -> dict[str, str | list[str]]:
    """
    Create an environment map.

    Returns:
        dict[str, str | list[str]]: A dictionary of variable names with a key.
    """
    env = {
        'XDG_CONFIG_HOME': os.path.join(os.getenv('HOME'), '.config'),
        'XDG_DATA_HOME': os.path.join(os.getenv('HOME'), '.local', 'share'),
        'CONFIG_DIR': user_config_directory(),
        'DATA_DIR': user_data_directory(),
    }
    for key, value in kwargs.items():
        env[key] = value
    return env

def environment_replace_command(command: list[str], environment: dict[str, str | list[str]]={}) -> list[str]:
    """
    Replace all variables in a command with the appropriate substitutions.

    Parameters:
        command (list[str]): The source command.
        environment (dict[str, str | list[str]]): The environment containing the variables.

    Returns:
        list[str]: The output command.
    """
    replaced = command.copy()
    items = environment.items()
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
