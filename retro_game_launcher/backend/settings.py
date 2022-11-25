import gi
from gi.repository import Gio
from retro_game_launcher.backend import constants

THEME = 'theme'
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

    ### THEME

    @property
    def theme(self) -> str:
        """
        Get the theme.

        Returns:
            str: The theme.
        """
        return self.__settings.get_string(THEME)

    @theme.setter
    def theme(self, theme: str) -> None:
        """
        Set the theme.

        Parameters:
            theme (str): The theme.
        """
        self.__settings.set_string(THEME, theme)

    def connect_theme_changed(self, function) -> None:
        self.__settings.connect('changed::%s' % THEME, function)

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

