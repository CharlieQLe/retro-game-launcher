import os
import gi
from gi.repository import Gio
from retro_game_launcher.backend import constants

def user_config_directory():
    """
    Get the directory for this project's configs.
    """
    xdg_config_home = os.getenv('XDG_CONFIG_HOME')
    if not xdg_config_home:
        xdg_config_home = os.path.join(os.getenv('HOME'), '.config')
    return os.path.join(xdg_config_home, constants.app_name)

def user_data_directory():
    """
    Get the directory for this project's data.
    """
    xdg_data_home = os.getenv('XDG_DATA_HOME')
    if not xdg_data_home:
        xdg_data_home = os.path.join(os.getenv('HOME'), '.local', 'share')
    return os.path.join(xdg_data_home, constants.app_name)

def environment_map(**kwargs):
    env = {
        'XDG_CONFIG_HOME': os.path.join(os.getenv('HOME'), '.config'),
        'XDG_DATA_HOME': os.path.join(os.getenv('HOME'), '.local', 'share'),
        'CONFIG_DIR': user_config_directory(),
        'DATA_DIR': user_data_directory(),
    }
    for key, value in kwargs.items():
        env[key] = value
    return env

def environment_replace_command(command, environment={}):
    replaced = command.copy()
    has_key = True
    while has_key:
        has_key = False
        for key in environment:
            env = '${%s}' % key
            value = environment[key]
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
