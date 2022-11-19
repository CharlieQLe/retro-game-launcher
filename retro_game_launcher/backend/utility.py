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

def environment_map(game_name=None):
    return {
        'XDG_CONFIG_HOME': os.path.join(os.getenv('HOME'), '.config'),
        'XDG_DATA_HOME': os.path.join(os.getenv('HOME'), '.local', 'share'),
        'CONFIG_DIR': user_config_directory(),
        'DATA_DIR': user_data_directory(),
        'GAME': game_name
    }

def environment_replace_string(string, environment={}):
    fixed_string = string
    has_key = True
    while has_key:
        has_key = Falsecommand
        for e in environment:
            env = '${%s}' % e
            value = environment[e]
            if value is not None:
                has_key = has_key or fixed_string.__contains__(env)
                fixed_string = fixed_string.replace(env, value)
    return fixed_string

def environment_replace_command(command, environment={}):
    replaced = command.copy()
    has_key = True
    while has_key:
        has_key = False
        for key in environment:
            env = '${%s}' % key
            value = environment[key]
            if value is not None:
                if env in replaced:
                    has_key = True
                    replaced[replaced.index(env)] = value
    return replaced
