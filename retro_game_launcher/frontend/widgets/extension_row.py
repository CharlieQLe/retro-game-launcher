import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesRowFactory

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/widgets/extension_row.ui')
class ExtensionRow(Adw.EntryRow):
    """
    Handles a row for extensions.
    """
    __gtype_name__ = 'ExtensionRow'
    __gsignals__ = {
        'remove_clicked': (GObject.SIGNAL_RUN_FIRST, None, (Adw.PreferencesRow,))
    }

    def __init__(self) -> None:
        """
        Initialize the row.
        """
        super().__init__()

    @Gtk.Template.Callback()
    def on_remove_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle clicking the remove button.

        Parameters:
            button (Gtk.Button): The button that was clicked.
        """
        self.emit('remove_clicked', self)

class ExtensionRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> ExtensionRow:
        return ExtensionRow()
