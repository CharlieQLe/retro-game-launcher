import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject

class DynamicPreferencesRowFactory:
    """
    The abstract definition for a factory that generates a row.
    """

    def create_row(self) -> Adw.PreferencesRow:
        """
        Create a preferences row.

        Returns:
            Adw.PreferencesRow: The row that was created.
        """
        raise NotImplementedError()

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/dynamic_preferences_group.ui')
class DynamicPreferencesGroup(Adw.PreferencesGroup):
    """
    Handle a dynamic preferences group.

    Attributes:
        can_user_add (bool): Can users manually add rows.
        add_btn_icon_name (str): The name of the add button's icon.
        add_btn_text (str): The text of the add button's label.
        empty_row_title (str): The title of the empty row.
    """

    __gtype_name__ = 'DynamicPreferencesGroup'
    __gsignals__ = {
        'row_added': (GObject.SIGNAL_RUN_FIRST, None, (Adw.PreferencesRow,))
    }

    empty_row = Gtk.Template.Child()

    can_user_add: bool = GObject.Property(type=bool, default=True)
    add_btn_icon_name: str = GObject.Property(type=str, default='')
    add_btn_text: str = GObject.Property(type=str, default='')
    empty_row_title: str = GObject.Property(type=str, default='')

    def __init__(self, **kwargs) -> None:
        """
        Initialize the group.
        """
        super().__init__(**kwargs)

        self.rows: list[Adw.PreferencesRow] = []
        self.factory: DynamicPreferencesRowFactory = None

    @Gtk.Template.Callback()
    def on_add_clicked(self, button: Gtk.Button) -> None:
        """
        Handle the add button.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        if self.factory is None:
            return
        row = self.factory.create_row()
        self.add_row(row)
        self.emit('row_added', row)

    def set_factory(self, factory: DynamicPreferencesRowFactory) -> None:
        """
        Set the factory for this group.

        Parameters:
            factory (DynamicPreferencesRowFactory): The factory to set
        """
        self.factory = factory

    def clear_rows(self) -> None:
        """
        Clear all the rows from this group.
        """
        for row in self.rows:
            self.remove(row)
        self.rows = []
        self.empty_row.show()

    def remove_row(self, row: Adw.PreferencesRow) -> bool:
        """
        Remove the row from the group.

        Parameters:
            row (Adw.PreferencesRow): The row to remove.

        Returns:
            bool: True if the row was removed, false if it wasn't.
        """
        if row in self.rows:
            self.remove(row)
            self.rows.remove(row)
            if len(self.rows) > 0:
                self.empty_row.hide()
            else:
                self.empty_row.show()
            return True
        return False

    def add_row(self, row: Adw.PreferencesRow) -> bool:
        """
        Add the row to this group.

        Parameters:
            row (Adw.PreferencesRow): The row to add.

        Returns:
            bool: True if the row was added, false if it wasn't.
        """
        if row in self.rows:
            return False
        self.add(row)
        self.rows.append(row)
        self.empty_row.hide()
        return True
