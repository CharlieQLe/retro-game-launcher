import gi
from gi.repository import Gio
from retro_game_launcher.backend import constants

TGDB_API_KEY = 'tgdb-api-key'

class Settings:
    """
    Handle the settings for this application's gschema.
    """

    @staticmethod
    def gsettings() -> Gio.Settings:
        """
        Get the settings schema for this application.

        Returns:
            Gio.Settings: The settings.
        """
        return Gio.Settings(schema_id=constants.app_id)

    ###

    def __init__(self) -> None:
        """
        Initialize the settings.
        """
        self.__settings = Settings.gsettings()

    ### THEGAMESDB

    @property
    def tgdb_api_key(self) -> str:
        """
        Get the API key for TheGamesDB.

        Returns:
            str: The API key.
        """
        return self.__settings.get_string(TGDB_API_KEY)

    @tgdb_api_key.setter
    def tgdb_api_key(self, key: str) -> None:
        """
        Set the API key for TheGamesDB.

        Parameters:
            key (str): The API key.
        """
        self.__settings.set_string(TGDB_API_KEY, key)

