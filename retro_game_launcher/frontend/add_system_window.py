import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/add_system_window.ui')
class AddSystemWindow(Adw.Window):
    __gtype_name__ = 'AddSystemWindow'
    __gsignals__ = {
        'add_system': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    toast_overlay = Gtk.Template.Child()
    add_system_btn = Gtk.Template.Child()
    system_name_entry = Gtk.Template.Child()
    games_directory_entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_system_btn.set_sensitive(False)
        self.games_directory_chooser = Gtk.FileChooserNative(
            title='Select a folder',
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            modal=True,
            select_multiple=False,
            accept_label='Select',
            cancel_label='Cancel',
            transient_for=self)
        self.games_directory_chooser.connect('response', self.games_directory_response)

    @Gtk.Template.Callback()
    def on_cancel_clicked(self, *args):
        self.close()

    @Gtk.Template.Callback()
    def on_add_system_clicked(self, *args):
        system_name = self.system_name_entry.get_text()
        games_directory = self.games_directory_entry.get_text()
        sc = SystemConfig(system_name, games_directory)
        sc.save()
        self.emit('add_system', system_name)
        self.close()

    @Gtk.Template.Callback()
    def on_system_entry_changed(self, *args):
        system_name = self.system_name_entry.get_text()
        games_directory = self.games_directory_entry.get_text()
        self.add_system_btn.set_sensitive(
            not SystemConfig.system_exists(system_name) and
            not system_name.startswith(' ') and
            not system_name.endswith(' ') and
            len(system_name) > 0 and
            os.path.isdir(games_directory))

    @Gtk.Template.Callback()
    def on_choose_games_directory_clicked(self, *args):
        self.games_directory_chooser.show()

    def games_directory_response(self, *args):
        if args[1] == Gtk.ResponseType.ACCEPT:
            file = self.games_directory_chooser.get_file()
            path = file.get_path()
            if path is not None:
                self.games_directory_entry.set_text(path)
