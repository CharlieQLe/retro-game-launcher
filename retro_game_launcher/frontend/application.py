import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib
from retro_game_launcher.backend import constants
from retro_game_launcher.frontend.main_window import MainWindow

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

    def on_handle_local_options(self, application, options) -> int:
        if options.contains("system"):
            self.arg_system = options.lookup_value("system").get_string()
        return -1

    def on_activate(self, application):
        """
        Activate the application.
        """
        win = MainWindow(
            arg_system=self.arg_system,
            application=application)
        win.present()
