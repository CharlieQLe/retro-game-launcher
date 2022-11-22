import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesRowFactory

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/widgets/key_value_row.ui')
class KeyValueRow(Adw.ActionRow):
    """
    Handles a row with two entry fields.
    """
    __gtype_name__ = 'KeyValueRow'
    __gsignals__ = {
        'key_value_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,str))
    }

    key_entry = Gtk.Template.Child()
    value_entry = Gtk.Template.Child()

    def __init__(self) -> None:
        """
        Initialize the row.
        """
        super().__init__()

    @Gtk.Template.Callback()
    def on_key_value_changed(self, _: Gtk.Entry) -> None:
        """
        Handles when the key or value was changed.

        Parameters:
            _ (Gtk.Entry): Unused
        """
        self.emit('key_value_changed', self.key_entry.get_text(), self.value_entry.get_text())

    @property
    def key(self) -> str:
        """
        Get the key.

        Returns:
            str: The key to get.
        """
        return self.key_entry.get_text()

    @key.setter
    def key(self, key: str) -> None:
        """
        Set the key.

        Parameters:
            key (str): The key to set.
        """
        self.key_entry.set_text(key)

    @property
    def value(self) -> str:
        """
        Get the value.

        Returns:
            str: The value to get.
        """
        return self.value_entry.get_text()

    @value.setter
    def value(self, value: str) -> None:
        """
        Set the value.

        Parameters:
            value (str): The value to set.
        """
        self.value_entry.set_text(value)

class KeyValueRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> KeyValueRow:
        return KeyValueRow()
