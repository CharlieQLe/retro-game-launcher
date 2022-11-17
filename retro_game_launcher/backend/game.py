import gi
from gi.repository import GObject

class Game(GObject.Object):
    __gtype_name__ = 'Game'

    def __init__(self, game_name, directory, game_file_name, config, cover_file_path):
        GObject.Object.__init__(self)
        self.game_name = game_name
        self.directory = directory
        self.game_file_name = game_file_name
        self.config = config
        self.cover_file_path = cover_file_path

