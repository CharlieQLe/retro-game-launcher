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

    def __init__(self, game_name: str, rom_path: str, thumbnail_path: str | None, config: SystemConfig) -> None:
        """
        Initialize the game object.

        Parameters:
            game_name (str): The name of the game.
            rom_path (str): The ROM file path.
            thumbnail_path (str): The thumbnail file path.
            config (SystemConfig): The system configuration.
        """
        GObject.Object.__init__(self)
        self.__process = None
        self.game_name = game_name
        self.rom_path = rom_path
        self.thumbnail_path = thumbnail_path
        self.config = config

    def get_thumbnail_path(self) -> str | None:
        """
        Get the path to the thumbnail file.

        Returns:
            str | None: The thumbnail path.
        """
        return self.thumbnail_path

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
        self.__process = subprocess.Popen(self.config.get_substituted_launch_command(GAME=self.rom_path))
        return self.__process

