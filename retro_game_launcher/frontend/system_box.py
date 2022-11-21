import os
import gi
import subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, Gtk, GObject
import retro_game_launcher.backend.constants as constants
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig
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
        self.emit('closed')

    @Gtk.Template.Callback()
    def on_refresh_btn_clicked(self, *args):
        self.reload_views()

    @Gtk.Template.Callback()
    def on_open_games_btn_clicked(self, *args):
        Gtk.show_uri(self.window, GLib.filename_to_uri(self.system_config.games_directory), Gdk.CURRENT_TIME)

    @Gtk.Template.Callback()
    def on_open_emu_btn_clicked(self, *args):
        subprocess.Popen(self.system_config.get_substituted_emulator_command())

    @Gtk.Template.Callback()
    def on_manage_btn_clicked(self, *args):
        self.pop_menu.popdown()
        pref = SystemPreferences(config=self.system_config)
        pref.set_transient_for(self.window)
        pref.present()

    @Gtk.Template.Callback()
    def on_delete_btn_clicked(self, *args):
        self.pop_menu.popdown()
        self.delete_dialog.show()

    def delete_response(self, *args):
        if args[1] == 'delete':
            self.emit('closed')
            self.emit('deleted', self.system_name)
        else:
            self.delete_dialog.hide()

    def reload_views(self):
        self.all_view.clear_games()
        for gm in self.system_config.load_games():
            self.window.toast_overlay.add_toast(Adw.Toast(title=_('%s could not be loaded!' % gm)))

        if len(self.system_config.games) == 0:
            return

        for game in self.system_config.games:
            self.all_view.add_game(Game(
                game_name=game.name,
                game_file_name=game.rom_path,
                thumbnail_file_name=game.thumbnail_path,
                config=self.system_config))
