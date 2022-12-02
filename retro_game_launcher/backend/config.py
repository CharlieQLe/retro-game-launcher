import json
import os
import sys
import shlex
import subprocess
from retro_game_launcher.backend import utility
from retro_game_launcher.backend import constants

class SystemConfig:
    @staticmethod
    def load(system_name: str) -> 'SystemConfig':
        """
        Load the system.

        Parameters:
            system_name (str): The name of the system.

        Returns:
            SystemConfig: The config if one exists, None otherwise.
        """
        if not SystemConfig.system_exists(system_name):
            return None
        sc = SystemConfig()
        sc.name = system_name
        sc.config_path = SystemConfig.generate_config_path(system_name)
        sc.reload()
        return sc

    @staticmethod
    def load_from_path(system_name, path: str):
        if not os.path.exists(path):
            return None
        sc = SystemConfig()
        sc.name = system_name
        sc.config_path = path
        sc.reload()
        return sc

    @staticmethod
    def delete(system_name: str) -> bool:
        """
        Delete system.

        Parameters:
            system_name (str): The name of the system.

        Returns:
            bool: True if the system was deleted, false otherwise.
        """
        if not SystemConfig.system_exists(system_name):
            return False
        os.remove(SystemConfig.generate_config_path(system_name))
        return True

    @staticmethod
    def get_system_names() -> list[str]:
        """
        Get the system names.

        Returns:
            list[str]: The list of systems.
        """
        return [f[:-5] for f in os.listdir(utility.user_config_directory()) if not os.path.isdir(f) and f.endswith('.json') and len(f) > 5]

    @staticmethod
    def system_exists(system_name: str) -> bool:
        """
        Check if the system exists.

        Parameters:
            system_name (str): The name of the system.

        Returns:
            bool: True if the system exists, false otherwise.
        """
        return system_name in SystemConfig.get_system_names()

    @staticmethod
    def generate_config_path(system_name: str) -> str:
        return os.path.join(utility.user_config_directory(), '%s.json' % system_name)

    ###

    def __init__(self) -> None:
        """
        Initialize the system.

        Parameters:
            system_name (str): The name of the system.
            games_directories (list[str]): The games directories.
        """
        self.__name = ''
        self.__config_path = ''
        self.__games = []
        self.__configuration = {
            'game_directories': [],
            'emulator_command': "",
            'launch_command': "${EMULATOR} ${GAME}",
            'images': {
                'thumbnail': {
                    'width': 256,
                    'height': 256
                }
            },
            'extensions': []
        }

    def reload(self) -> None:
        """
        Reload the configuration.
        """
        with open(self.__config_path, 'r') as f:
            self.__configuration = json.load(f)

    def save(self) -> None:
        """
        Save the configuration.
        """
        with open(self.__config_path, 'w') as f:
            json.dump(self.__configuration, f, indent=4)

    ### PROPERTIES

    @property
    def name(self) -> str:
        """
        Get the name of the system.

        Returns:
            str: The system name.
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> str:
        """
        Set the name of the system.

        Properties:
            name (str): The system name.
        """
        self.__name = name

    @property
    def config_path(self) -> str:
        """
        Get the path to the system config.

        Returns:
            str: The path.
        """
        return self.__config_path

    @config_path.setter
    def config_path(self, path: str) -> str:
        """
        Set the path to the system config.

        Properties:
            path (str): The system name.
        """
        self.__config_path = path

    @property
    def game_directories(self) -> list[str]:
        """
        Get the game directories.

        Returns:
            list[str]: The game directories.
        """
        return self.__configuration['game_directories']

    @game_directories.setter
    def game_directories(self, directories: list[str]) -> None:
        """
        Set the games directory.

        Parameters:
            directories (list[str]): The directories to set.
        """
        self.__configuration['game_directories'] = directories

    @property
    def extensions(self) -> list[str]:
        """
        Get the extensions.

        Returns:
            list[str]: The extensions to get.
        """
        return self.__configuration['extensions']

    @extensions.setter
    def extensions(self, extensions: list[str]) -> None:
        """
        Set the extensions.

        Parameters:
            extensions (list[str]): The extensions to set.
        """
        self.__configuration['extensions'] = list(dict.fromkeys(extensions))

    @property
    def emulator_command(self) -> str:
        """
        Get the emulator command.

        Returns:
            str: The command to get.
        """
        return self.__configuration['emulator_command']

    @emulator_command.setter
    def emulator_command(self, command: str) -> None:
        """
        Set the emulator command.

        Parameters:
            command (str): The command to set.
        """
        self.__configuration['emulator_command'] = command

    @property
    def launch_command(self) -> str:
        """
        Get the launch command.

        Returns:
            str: The command to get.
        """
        return self.__configuration['launch_command']

    @launch_command.setter
    def launch_command(self, command: str) -> None:
        """
        Set the launch command.

        Parameters:
            command (str): The command to set.
        """
        self.__configuration['launch_command'] = command

    @property
    def image_thumbnail_size(self) -> tuple[int, int]:
        """
        Get the image thumbnail size.

        Returns:
            tuple[int, int]: The size of the thumbnail.
        """
        thumbnail = self.__configuration['images']['thumbnail']
        return (thumbnail['width'], thumbnail['height'])

    @image_thumbnail_size.setter
    def image_thumbnail_size(self, size: tuple[int, int]) -> None:
        """
        Set the image thumbnail size.

        Parameters:
            size (tuple[int, int]): The size of the thumbnail.
        """
        thumbnail = self.__configuration['images']['thumbnail']
        thumbnail['width'] = size[0]
        thumbnail['height'] = size[1]

    @property
    def games(self) -> list['GameConfig']:
        """
        Get the currently loaded games.

        Returns:
            list[GameConfig]: The game configs.
        """
        return self.__games

    ### GAMES

    def has_game(self, game_name: str) -> bool:
        """
        Check if the game exists.

        Parameters:
            game_name (str): The game name.

        Returns:
            bool: Whether or not the game exists.
        """
        return any(game_name in os.listdir(dir) and os.path.isdir() for dir in self.game_directories)

    def get_game_directory(self, game_name: str) -> str | None:
        """
        Get the directory path for the given game name.

        Parameters:
            game_name (str): The game name.

        Returns:
            str | None: The path to the game if it exists, otherwise None.
        """
        for dir in self.game_directories:
            if game_name in os.listdir(dir):
                path = os.path.join(dir, game_name)
                if os.path.isdir(path):
                    return path
        return None

    def get_game_paths(self) -> list[str]:
        subfolders = []
        for dir in self.game_directories:
            subfolders.extend(list(filter(lambda d : os.path.isdir(d), [ os.path.join(dir, d) for d in os.listdir(dir) ])))
        return subfolders

    def load_games(self) -> list['GameConfig']:
        """
        Load games into the system, clearing all existing games.

        Returns:
            list['GameConfig']: All loaded games.
        """
        self.__games = []
        self.game_errors = []
        for game_path in self.get_game_paths():
            try:
                game = GameConfig(game_path, self)
                if not game.hidden:
                    self.__games.append(game)
            except:
                self.game_errors.append(os.path.basename(game_path))
        return self.game_errors

    ### COMMANDS

    def run_launch_command(self, rom_path: str) -> subprocess.Popen | None:
        command = self.launch_command
        command = command.replace('${EMULATOR}', self.emulator_command)
        command = command.replace('${GAME}', '"%s"' % rom_path)
        split_command = shlex.split(command)
        split_command.insert(0, '--host')
        split_command.insert(0, '/usr/bin/flatpak-spawn')
        return subprocess.Popen(split_command)

    def run_emulator_command(self) -> subprocess.Popen | None:
        split_command = shlex.split(self.emulator_command)
        split_command.insert(0, '--host')
        split_command.insert(0, '/usr/bin/flatpak-spawn')
        return subprocess.Popen(split_command)

class NoGameExists(Exception):
    """
    Raise this for GameConfig.
    """
    pass

class GameConfig:
    """
    The configuration for a game.

    Read-Only Properties:
        name (str): The name of the game.
        rom_path (str): The path to the rom.
        thumbnail_path (str): The path to the thumbnail.
        hidden (bool): Whether or not the game should be ignored.
    """

    def __init__(self, game_path: str, system_config: SystemConfig) -> None:
        """
        Initialize the config.

        Parameters:
            game_path (str): The path to the game.
            system_config (SystemConfig): The system configuration.
        """
        if not os.path.isdir(game_path):
            raise NoGameExists()

        self.__name = os.path.basename(game_path)
        game_subfolder_contents = os.listdir(game_path)

        # Handle hidden
        self.__hidden = 'hidden' in game_subfolder_contents

        # Handle ROM
        game_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in system_config.extensions), game_subfolder_contents))
        if not self.__hidden and len(game_files) == 0:
            raise NoGameExists()
        self.__rom_path = os.path.join(game_path, game_files[0]) if len(game_files) > 0 else None

        # Handle thumbnail
        thumbnail_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in constants.cover_extensions), game_subfolder_contents))
        self.__thumbnail_path = os.path.join(game_path, thumbnail_files[0]) if len(thumbnail_files) > 0 else None

    @property
    def name(self) -> str:
        """
        Get the name of the game.

        Returns:
            str: The name of the game.
        """
        return self.__name

    @property
    def rom_path(self) -> str:
        """
        Get the path to the ROM.

        Returns:
            str: The path to the ROM.
        """
        return self.__rom_path

    @property
    def thumbnail_path(self) -> str | None:
        """
        Get the path to the thumbnail.

        Returns:
            str | None: The path to the thumbnail if it exists, otherwise return None.
        """
        return self.__thumbnail_path

    @property
    def hidden(self) -> bool:
        """
        Get if this game is hidden.

        Returns:
            bool: Whether or not the game is hidden.
        """
        return self.__hidden
