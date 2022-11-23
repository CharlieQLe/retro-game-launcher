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

    def __init__(self) -> None:
        """
        Initialize the row.
        """
        super().__init__()

class ExtensionRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> ExtensionRow:
        return ExtensionRow()
