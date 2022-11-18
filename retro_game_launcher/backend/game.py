import os
import subprocess
import gi
from gi.repository import GObject
from retro_game_launcher.backend import utility

class Game(GObject.Object):
    __gtype_name__ = 'Game'

    process = None

    def __init__(self, game_name, game_file_name, thumbnail_file_name, config):
        GObject.Object.__init__(self)
        self.game_name = game_name
        self.game_file_name = game_file_name
        self.config = config
        self.thumbnail_file_name = thumbnail_file_name

    def get_directory(self):
        return os.path.join(self.config.get_games_dir(), self.game_name)

    def get_game_path(self):
        return os.path.join(self.get_directory(), self.game_file_name)

    def get_thumbnail_path(self):
        return None if self.thumbnail_file_name is None else os.path.join(self.get_directory(), self.thumbnail_file_name)

    def run(self):
        if self.process is not None:
            if self.process.poll() is None:
                return None
            else:
                self.process = None
        command = ['/usr/bin/flatpak-spawn', '--host']
        for x in self.config.get_launch_command().split():
            command.append(x)
        env = utility.environment_map(game_name=self.get_game_path())
        for i in range(len(command)):
            command[i] = utility.environment_replace(command[i], env)
        self.process = subprocess.Popen(command)
        return self.process

