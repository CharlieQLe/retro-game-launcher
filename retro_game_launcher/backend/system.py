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
        self._name = system_name
        self._config_path = os.path.join(utility.user_config_directory(), '%s.json' % system_name)
        self._configuration = {
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
        }

    def reload(self):
        with open(self._config_path, 'r') as f:
            self._configuration = json.load(f)

    def save(self):
        with open(self._config_path, 'w') as f:
            json.dump(self._configuration, f, indent=4)

    ### PROPERTIES

    def name(self):
        return self._name

    ### GETTERS

    def get_games_dir(self):
        return self._configuration['games_directory']

    def get_extensions(self):
        return self._configuration['extensions']

    def get_emulator_command(self):
        return self._configuration['emulator_command']

    def get_launch_command(self):
        return self._configuration['launch_command']

    def get_launch_vars(self):
        return self._configuration['launch_vars']

    def get_image_thumbnail_size(self):
        thumbnail = self._configuration['images']['thumbnail']
        return (thumbnail['width'], thumbnail['height'])

    ### SETTERS

    def set_games_dir(self, games_directory):
        self._configuration['games_directory'] = games_directory

    def set_extensions(self, extensions):
        self._configuration['extensions'] = extensions

    def set_emulator_command(self, emulator_command):
        self._configuration['emulator_command'] = emulator_command

    def set_launch_command(self, launch_command):
        self._configuration['launch_command'] = launch_command

    def set_launch_var(self, key, value):
        self._configuration['launch_vars'][key] = value

    def set_image_thumbnail_size(self, width, height):
        thumbnail = self._configuration['images']['thumbnail']
        thumbnail['width'] = width
        thumbnail['height'] = height

    ### GAMES

    def get_game_subfolders(self):
        dir = self.get_games_dir()
        if not os.path.isdir(dir):
            return []
        return [ d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d)) ]
