import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib
from retro_game_launcher.backend import constants
from retro_game_launcher.frontend.main_window import MainWindow
from retro_game_launcher.frontend.preferences import Preferences

class RetroGameLauncherApp(Adw.Application):
    arg_system = None

    def __init__(self):
        super().__init__(application_id=constants.app_id)
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_pref_action)
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

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Retro Game Launcher',
                                application_icon='applications-games-symbolic',
                                developer_name='Charlie Le',
                                version='0.1.0',
                                developers=['Charlie Le'],
                                copyright='© 2022 Charlie Le')
        about.present()

    def on_pref_action(self, widget, _):
        pref = Preferences()
        pref.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

