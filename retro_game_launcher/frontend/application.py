import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib
from retro_game_launcher.backend import constants
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.backend.settings import Settings
from retro_game_launcher.frontend.main_window import MainWindow
from retro_game_launcher.frontend.minimal_window import MinimalWindow

class RetroGameLauncherApp(Adw.Application):
    """
    Handles the application.

    Attributes:
        arg_system (str | None): The name of the system to display on launch.
    """

    arg_system: str | None = None

    def __init__(self):
        """
        Initialize this application.
        """
        super().__init__(application_id=constants.app_id)

        self.connect('handle-local-options', self.on_handle_local_options)
        self.connect('activate', self.on_activate)

        self.add_main_option(
            long_name='system',
            short_name=ord('s'),
            flags=GLib.OptionFlags.NONE,
            arg=GLib.OptionArg.STRING,
            description=_('Launch a system'),
            arg_description='Load the corresponding system page if one exists.')

        self.__settings = Settings()
        self.__settings.connect_theme_changed(self.on_theme_changed)
        self.__style_manager = self.get_style_manager()
        self.on_theme_changed(None, None)

    def on_handle_local_options(self, application, options) -> int:
        if options.contains("system"):
            self.arg_system = options.lookup_value("system").get_string()
        return -1

    def on_activate(self, application):
        """
        Activate the application.
        """
        if self.arg_system is not None and SystemConfig.system_exists(self.arg_system):
            MinimalWindow(self.arg_system, application=application).present()
        else:
            MainWindow(application=application).present()
            
    def on_theme_changed(self, settings: Gio.Settings, setting_name: str) -> None:
        if self.__settings.theme == 'force-light':
            self.__style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif self.__settings.theme == 'force-dark':
            self.__style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        elif self.__settings.theme == 'prefer-dark':
            self.__style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        elif self.__settings.theme == 'prefer-light':
            self.__style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)
        else:
            self.__style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
