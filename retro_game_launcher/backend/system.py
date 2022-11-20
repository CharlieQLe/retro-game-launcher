import json
import os
import sys
from retro_game_launcher.backend import utility

class SystemConfig:
    @staticmethod
    def load(system_name):
        if not SystemConfig.system_exists(system_name):
            return None
        sc = SystemConfig(system_name)
        sc.reload()
        return sc

    @staticmethod
    def delete(system_name):
        if not SystemConfig.system_exists(system_name):
            return False
        os.remove(os.path.join(utility.user_config_directory(), '%s.json' % system_name))
        return True

    @staticmethod
    def get_system_names():
        return [f[:-5] for f in os.listdir(utility.user_config_directory()) if not os.path.isdir(f) and f.endswith('.json') and len(f) > 5]

    @staticmethod
    def system_exists(system_name):
        return system_name in SystemConfig.get_system_names()

    ###

    def __init__(self, system_name, games_directory=''):
        self.__name = system_name
        self.__config_path = os.path.join(utility.user_config_directory(), '%s.json' % system_name)
        self.__configuration = {
            'games_directory': games_directory,
            'emulator_command': [
                'INSERT_COMMAND_HERE'
            ],
            'launch_command': [
                '${EMULATOR}',
                'INSERT_OPTIONS_HERE',
                '${GAME}'
            ],
            'launch_vars': {},
            'images': {
                'thumbnail': {
                    'width': 256,
                    'height': 256
                }
            },
            'extensions': [],
            'recent_games': [],
        }

    def reload(self):
        with open(self.__config_path, 'r') as f:
            self.__configuration = json.load(f)

    def save(self):
        with open(self.__config_path, 'w') as f:
            json.dump(self.__configuration, f, indent=4)

    ### PROPERTIES

    @property
    def name(self):
        return self.__name

    @property
    def games_directory(self) -> str:
        return self.__configuration['games_directory']

    @games_directory.setter
    def games_directory(self, directory: str):
        self.__configuration['games_directory'] = directory

    @property
    def extensions(self) -> list:
        return self.__configuration['extensions']

    @extensions.setter
    def extensions(self, extensions: list):
        self.__configuration['extensions'] = list(dict.fromkeys(extensions))

    @property
    def emulator_command(self) -> list:
        return self.__configuration['emulator_command']

    @emulator_command.setter
    def emulator_command(self, command: list) -> list:
        self.__configuration['emulator_command'] = command

    @property
    def launch_command(self) -> list:
        return self.__configuration['launch_command']

    @launch_command.setter
    def launch_command(self, command: list):
        self.__configuration['launch_command'] = command

    @property
    def image_thumbnail_size(self) -> tuple:
        thumbnail = self.__configuration['images']['thumbnail']
        return (thumbnail['width'], thumbnail['height'])

    @image_thumbnail_size.setter
    def image_thumbnail_size(self, size: tuple):
        thumbnail = self.__configuration['images']['thumbnail']
        thumbnail['width'] = size[0]
        thumbnail['height'] = size[1]

    @property
    def recent_games(self) -> list:
        return self.__configuration['recent_games']

    @recent_games.setter
    def recent_games(self, games: list):
        self.__configuration['recent_games'] = recent_games

    ### GAMES

    def get_game_subfolders(self):
        dir = self.games_directory
        return [ d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d)) ] if os.path.isdir(dir) else []
