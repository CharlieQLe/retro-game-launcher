import os
import gi
import subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, Gtk, GObject
import retro_game_launcher.backend.constants as constants
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.system import SystemConfig
from retro_game_launcher.backend.game import Game
from retro_game_launcher.frontend.system_preferences import SystemPreferences
from retro_game_launcher.frontend.game_view import GameView

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_box.ui')
class SystemBox(Gtk.Box):
    __gtype_name__ = 'SystemBox'
    __gsignals__ = {
        'closed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'deleted': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    system_name = GObject.Property(type=str, default='')

    go_back_btn = Gtk.Template.Child()
    refresh_btn = Gtk.Template.Child()
    all_view = Gtk.Template.Child()
    pop_menu = Gtk.Template.Child()
    manage_btn = Gtk.Template.Child()
    delete_btn = Gtk.Template.Child()

    def __init__(self, system_name, application, window, only_system=False, **kwargs):
        super().__init__(**kwargs)

        self.system_name = system_name
        self.application = application
        self.window = window

        if only_system:
            self.delete_btn.hide()
            self.go_back_btn.hide()

        self.system_config = SystemConfig.load(system_name)
        self.all_view.set_system_config(self.system_config)

        self.manage_btn.connect('clicked', self.manage_system)
        self.delete_btn.connect('clicked', self.delete_system)

        self.delete_dialog = Adw.MessageDialog(
            modal=True,
            heading='Delete %s?' % system_name,
            body='This cannot be undone! Are you sure you want to delete %s?' % system_name)
        self.delete_dialog.add_response('cancel', _('_Cancel'))
        self.delete_dialog.add_response('delete', _('_Delete'))
        self.delete_dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        self.delete_dialog.set_transient_for(window)
        self.delete_dialog.connect('response', self.delete_response)

        self.reload_views()

    @Gtk.Template.Callback()
    def on_go_back_btn_clicked(self, *args):
        self.on_closed()

    @Gtk.Template.Callback()
    def on_refresh_btn_clicked(self, *args):
        self.reload_views()

    @Gtk.Template.Callback()
    def on_open_games_btn_clicked(self, *args):
        Gtk.show_uri(self.window, GLib.filename_to_uri(self.system_config.games_directory), Gdk.CURRENT_TIME)

    @Gtk.Template.Callback()
    def on_open_emu_btn_clicked(self, *args):
        command = utility.environment_replace_command(self.system_config.emulator_command, utility.environment_map())
        command.insert(0, '--host')
        command.insert(0, '/usr/bin/flatpak-spawn')
        subprocess.Popen(command)

    def on_closed(self):
        self.emit('closed')

    def manage_system(self, *args):
        self.pop_menu.popdown()
        pref = SystemPreferences(config=self.system_config)
        pref.set_transient_for(self.window)
        pref.present()

    def delete_system(self, *args):
        self.pop_menu.popdown()
        self.delete_dialog.show()

    def delete_response(self, *args):
        if args[1] == 'delete':
            self.on_closed()
            self.emit('deleted', self.system_name)
        else:
            self.delete_dialog.hide()

    def reload_views(self):
        self.all_view.clear_games()
        game_subfolders = self.system_config.get_game_subfolders()
        if len(game_subfolders) == 0:
            return

        games_directory = self.system_config.games_directory
        extensions = self.system_config.extensions
        for game_subfolder in game_subfolders:
            game_subfolder_dir = os.path.join(games_directory, game_subfolder)
            game_subfolder_contents = os.listdir(game_subfolder_dir)
            game_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in extensions), game_subfolder_contents))
            if len(game_files) == 0:
                continue
            cover_files = list(filter(lambda file_name : any(file_name.endswith('.%s' % ext) for ext in constants.cover_extensions), game_subfolder_contents))
            self.all_view.add_game(Game(
                game_name=game_subfolder,
                game_file_name=game_files[0],
                thumbnail_file_name=cover_files[0] if len(cover_files) > 0 else None,
                config=self.system_config))
