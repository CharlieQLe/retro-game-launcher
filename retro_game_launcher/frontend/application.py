import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib
from retro_game_launcher.backend import constants
from retro_game_launcher.frontend.main_window import MainWindow

class RetroGameLauncherApp(Adw.Application):
    arg_system = None

    def __init__(self):
        super().__init__(application_id=constants.app_id)
        self.add_main_option(
            long_name='system',
            short_name=ord('s'),
            flags=GLib.OptionFlags.NONE,
            arg=GLib.OptionArg.STRING,
            description=_('Launch a system'),
            arg_description=None)

    def do_command_line(self, command):
        commands = command.get_options_dict()

        if commands.contains("system"):
            self.arg_system = commands.lookup_value("system").get_string()

        self.do_activate()
        return 0

    def do_activate(self):
        win = MainWindow(
            arg_system=self.arg_system,
            application=self)
        win.present()
