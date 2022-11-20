import json
import os
import sys
from retro_game_launcher.backend import utility
from retro_game_launcher.backend import constants

class SystemConfig:
    @staticmethod
    def load(system_name: str):
        if not SystemConfig.system_exists(system_name):
            return None
        sc = SystemConfig(system_name)
        sc.reload()
        return sc

    @staticmethod
    def delete(system_name: str) -> bool:
        if not SystemConfig.system_exists(system_name):
            return False
        os.remove(os.path.join(utility.user_config_directory(), '%s.json' % system_name))
        return True

    @staticmethod
    def get_system_names() -> list:
        return [f[:-5] for f in os.listdir(utility.user_config_directory()) if not os.path.isdir(f) and f.endswith('.json') and len(f) > 5]

    @staticmethod
    def system_exists(system_name: str) -> bool:
        return system_name in SystemConfig.get_system_names()

    ###

    def __init__(self, system_name: str, games_directory=''):
        self.__name = system_name
        self.__config_path = os.path.join(utility.user_config_directory(), '%s.json' % system_name)
        self.__games = []
        self.__configuration = {
            'games_directory': games_directory,
            'emulator_command': [
                '${CMD_EMULATOR}'
            ],
            'launch_command': [
                '${CMD_EMULATOR}',
                '${GAME}'
            ],
            'launch_var': {
                'CMD_EMULATOR': [
                    'INSERT_COMMAND_HERE'
                ]
            },
            'images': {
                'thumbnail': {
                    'width': 256,
                    'height': 256
                }
            },
            'extensions': []
        }

    def reload(self):
        with open(self.__config_path, 'r') as f:
            self.__configuration = json.load(f)

    def save(self):
        with open(self.__config_path, 'w') as f:
            json.dump(self.__configuration, f, indent=4)

    ### PROPERTIES

    @property
    def name(self) -> str:
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
    def launch_var(self) -> dict:
        return self.__configuration['launch_var']

    @launch_var.setter
    def launch_var(self, var: dict):
        self.__configuration['launch_var'] = var

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
    def games(self) -> list:
        return self.__games

    ### GAMES

    def has_game(self, game_name: str) -> bool:
        dir = self.games_directory
        return game_name in os.listdir(dir) and os.path.isdir(os.path.join(dir, game_name))

    def get_game_directory(self, game_name: str) -> str | None:
        return os.path.join(self.games_directory, game_name) if self.has_game(game_name) else None

    def get_game_subfolders(self) -> list:
        dir = self.games_directory
        return [ d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d)) ] if os.path.isdir(dir) else []

    def load_games(self) -> list:
        self.__games = []
        self.game_errors = []
        for gm in self.get_game_subfolders():
            try:
                g = GameConfig(gm, self)
                if not g.hidden:
                    self.__games.append(g)
            except:
                self.game_errors.append(gm)
        return self.game_errors

    ### COMMANDS

    def substitute_command(self, command, **kwargs):
        env_map = utility.environment_map(**kwargs)
        for key, value in self.launch_var.items():
            env_map[key] = value
        return utility.environment_replace_command(command, env_map)

    def get_substituted_launch_command(self, **kwargs):
        command = self.substitute_command(self.launch_command, **kwargs)
        command.insert(0, '--host')
        command.insert(0, '/usr/bin/flatpak-spawn')
        return command

    def get_substituted_emulator_command(self, **kwargs):
        command = self.substitute_command(self.emulator_command, **kwargs)
        command.insert(0, '--host')
        command.insert(0, '/usr/bin/flatpak-spawn')
        return command

class NoGameExists(Exception):
    pass

class GameConfig:
    def __init__(self, game_name: str, system_config: SystemConfig):
        self.__name = game_name
        game_directory = system_config.get_game_directory(game_name)
        if game_directory is None:
            raise NoGameExists()
        game_subfolder_contents = os.listdir(game_directory)

        # Handle hidden
        self.__hidden = 'hidden' in game_subfolder_contents

        # Handle ROM
        game_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in system_config.extensions), game_subfolder_contents))
        if not self.__hidden and len(game_files) == 0:
            raise NoGameExists()
        self.__rom_path = os.path.join(game_directory, game_files[0]) if len(game_files) > 0 else None

        # Handle thumbnail
        thumbnail_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in constants.cover_extensions), game_subfolder_contents))
        self.__thumbnail_path = thumbnail_files[0] if len(thumbnail_files) > 0 else None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def rom_path(self) -> str:
        return self.__rom_path

    @property
    def thumbnail_path(self) -> str | None:
        return self.__thumbnail_path

    @property
    def hidden(self) -> bool:
        return self.__hidden
