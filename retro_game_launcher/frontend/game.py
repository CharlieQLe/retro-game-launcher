import os
import subprocess
import gi
from gi.repository import GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig

class Game(GObject.Object):
    """
    Handles the game GObject.
    """
    __gtype_name__ = 'Game'

    def __init__(self, game_name: str, game_file_name: str, thumbnail_file_name: str, config: SystemConfig) -> None:
        """
        Initialize the game object.

        Parameters:
            game_name (str): The name of the game.
            game_file_name (str): The ROM file name.
            thumbnail_file_name (str): The thumbnail file name.
            config (SystemConfig): The system configuration.
        """
        GObject.Object.__init__(self)
        self.__process = None
        self.game_name = game_name
        self.game_file_name = game_file_name
        self.config = config
        self.thumbnail_file_name = thumbnail_file_name

    def get_directory(self) -> str:
        """
        Get the directory for the game.

        Returns:
            str: The directory path.
        """
        return os.path.join(self.config.games_directory, self.game_name)

    def get_game_path(self) -> str:
        """
        Get the path to the game ROM.

        Returns:
            str: The ROM path.
        """
        return os.path.join(self.get_directory(), self.game_file_name)

    def get_thumbnail_path(self) -> str:
        """
        Get the path to the thumbnail file.

        Returns:
            str: The thumbnail path.
        """
        return None if self.thumbnail_file_name is None else os.path.join(self.get_directory(), self.thumbnail_file_name)

    def run(self) -> subprocess.Popen | None:
        """
        Run the game.

        Returns:
            subprocess.Popen | None: None if the game failed to run, the process otherwise.
        """
        if self.__process is not None:
            if self.__process.poll() is None:
                return None
            else:
                self.__process = None
        self.__process = subprocess.Popen(self.config.get_substituted_launch_command(GAME=self.get_game_path()))
        return self.__process

