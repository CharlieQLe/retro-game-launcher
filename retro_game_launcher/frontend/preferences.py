import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from retro_game_launcher.backend.settings import Settings

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/preferences.ui')
class Preferences(Adw.PreferencesWindow):
    __gtype_name__ = 'Preferences'

    tgdb_key_entry = Gtk.Template.Child()

    def __init__(self, **kargs):
        super().__init__(**kargs)

        self.settings = Settings()

        self.tgdb_key_entry.set_text(self.settings.tgdb_api_key)

    @Gtk.Template.Callback()
    def on_tgdb_key_entry_changed(self, *args):
        self.settings.tgdb_api_key = self.tgdb_key_entry.get_text()
