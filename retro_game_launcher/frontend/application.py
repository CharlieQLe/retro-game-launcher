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

        self.add_main_option(
            long_name='system',
            short_name=ord('s'),
            flags=GLib.OptionFlags.NONE,
            arg=GLib.OptionArg.STRING,
            description=_('Launch a system'),
            arg_description=None)

    def do_command_line(self, command):
        """
        Handle command line arguments.

        Parameters:
            command (Gio.ApplicationCommandLine): The command options available.

        Returns:
            int
        """
        commands = command.get_options_dict()

        # Get the system name
        if commands.contains("system"):
            self.arg_system = commands.lookup_value("system").get_string()

        self.do_activate()
        return 0

    def do_activate(self):
        """
        Activate the application.
        """
        win = MainWindow(
            arg_system=self.arg_system,
            application=self)
        win.present()
