import gi
from gi.repository import Gio
from retro_game_launcher.backend import constants
from retro_game_launcher.backend import setting_keys

class Settings:
    @staticmethod
    def gsettings():
        return Gio.Settings(schema_id=constants.app_id)

    ###

    def __init__(self):
        self.settings = Settings.gsettings()

    ### THEGAMESDB

    def get_tgdb_api_key(self) -> str:
        return self.settings.get_string(setting_keys.TGDB_API_KEY)

    def set_tgdb_api_key(self, key):
        self.settings.set_string(setting_keys.TGDB_API_KEY, key)

    tgdb_api_key = property(get_tgdb_api_key, set_tgdb_api_key)

