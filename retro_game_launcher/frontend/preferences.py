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

    theme_dropdown: Gtk.DropDown = Gtk.Template.Child()
    tgdb_key_entry: Adw.EntryRow = Gtk.Template.Child()

    def __init__(self, **kargs) -> None:
        """
        Initialize preferences.
        """
        super().__init__(**kargs)

        self.theme_dropdown.connect('notify::selected', self.on_theme_dropdown_notify_selected)

        self.settings: Settings = Settings()
        self.tgdb_key_entry.set_text(self.settings.tgdb_api_key)

    def on_theme_dropdown_notify_selected(self, dropdown, selected):
        selected_pos = self.theme_dropdown.get_selected()
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
