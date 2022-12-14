import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from retro_game_launcher.backend.settings import Settings

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/preferences.ui')
class Preferences(Adw.PreferencesWindow):
    """
    Handles preferences.

    Attributes:
        settings (Settings): Handles the settings for this application.
    """
    __gtype_name__ = 'Preferences'

    theme_selector: Adw.ComboRow = Gtk.Template.Child()
    tgdb_key_entry: Adw.EntryRow = Gtk.Template.Child()

    def __init__(self, **kargs) -> None:
        """
        Initialize preferences.
        """
        super().__init__(**kargs)

        self.settings: Settings = Settings()

        if self.settings.theme == 'force-light':
            self.theme_selector.set_selected(1)
        elif self.settings.theme == 'force-dark':
            self.theme_selector.set_selected(2)
        else:
            self.theme_selector.set_selected(0)

        self.tgdb_key_entry.set_text(self.settings.tgdb_api_key)

    @Gtk.Template.Callback()
    def on_theme_notify_selected(self, row, selected):
        selected_pos = row.get_selected()
        if selected_pos == 1:
            self.settings.theme = 'force-light'
        elif selected_pos == 2:
            self.settings.theme = 'force-dark'
        else:
            self.settings.theme = 'prefer-light'

    @Gtk.Template.Callback()
    def on_tgdb_key_entry_changed(self, entry: Adw.EntryRow) -> None:
        """
        Handle changing the entry for TheGamesDB API Key.

        Parameters:
            entry (Adw.EntryRow): The entry row that was changed.
        """
        self.settings.tgdb_api_key = self.tgdb_key_entry.get_text()
