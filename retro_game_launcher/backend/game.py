import os
import subprocess
import gi
from gi.repository import GObject
from retro_game_launcher.backend import utility

class Game(GObject.Object):
    __gtype_name__ = 'Game'

    process = None

    def __init__(self, game_name, directory, game_file_name, config, cover_file_path):
        GObject.Object.__init__(self)
        self.game_name = game_name
        self.directory = directory
        self.game_file_name = game_file_name
        self.config = config
        self.cover_file_path = cover_file_path
        self.game_file_path = os.path.join(self.directory, self.game_file_name)

    def run(self):
        if self.process is not None:
            if self.process.poll() is None:
                return None
            else:
                self.process = None
        command = ['/usr/bin/flatpak-spawn', '--host']
        for x in self.config.get_launch_command().split():
            command.append(x)
        env = utility.environment_map(game_name=self.game_file_path)
        for i in range(len(command)):
            command[i] = utility.environment_replace(command[i], env)
        self.process = subprocess.Popen(command)
        return self.process

