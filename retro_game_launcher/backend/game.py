import os
import subprocess
import gi
from gi.repository import GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig

class Game(GObject.Object):
    __gtype_name__ = 'Game'

    __process = None

    def __init__(self, game_name, game_file_name, thumbnail_file_name, config: SystemConfig):
        GObject.Object.__init__(self)
        self.game_name = game_name
        self.game_file_name = game_file_name
        self.config = config
        self.thumbnail_file_name = thumbnail_file_name

    def get_directory(self):
        return os.path.join(self.config.games_directory, self.game_name)

    def get_game_path(self):
        return os.path.join(self.get_directory(), self.game_file_name)

    def get_thumbnail_path(self):
        return None if self.thumbnail_file_name is None else os.path.join(self.get_directory(), self.thumbnail_file_name)

    def run(self):
        if self.__process is not None:
            if self.__process.poll() is None:
                return None
            else:
                self.__process = None
        self.__process = subprocess.Popen(self.config.get_substituted_launch_command(GAME=self.get_game_path()))
        return self.__process

