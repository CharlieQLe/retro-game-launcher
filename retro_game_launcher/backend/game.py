import os
import subprocess
import gi
from gi.repository import GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.system import SystemConfig

class Game(GObject.Object):
    __gtype_name__ = 'Game'

    process = None

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
        if self.process is not None:
            if self.process.poll() is None:
                return None
            else:
                self.process = None
        command = ['/usr/bin/flatpak-spawn', '--host']
        for x in self.config.launch_command:
            command.append(x)
        env = utility.environment_map(game_name=self.get_game_path())
        emulator_cmd = utility.environment_replace_command(self.config.get_emulator_command(), env)
        cmd = utility.environment_replace_command(command, env)
        if '${EMULATOR}' not in cmd:
            return None
        index = cmd.index('${EMULATOR}')
        cmd.remove('${EMULATOR}')
        for i in range(len(emulator_cmd)):
            cmd.insert(index + i, emulator_cmd[i])
        self.process = subprocess.Popen(cmd)
        return self.process

