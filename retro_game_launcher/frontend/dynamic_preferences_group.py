import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject

class DynamicPreferencesRowFactory(GObject.Object):
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
        'row-added': (GObject.SIGNAL_RUN_FIRST, None, (Adw.PreferencesRow,)),
        'row-removed': (GObject.SIGNAL_RUN_FIRST, None, (Adw.PreferencesRow,))
    }

    can_user_add: bool = GObject.Property(type=bool, default=True)
    add_btn_icon_name: str = GObject.Property(type=str, default='')
    add_btn_text: str = GObject.Property(type=str, default='')
    empty_row_title: str = GObject.Property(type=str, default='')
    is_empty: bool = GObject.Property(type=bool, default=True)

    def __init__(self, **kwargs) -> None:
        """
        Initialize the group.
        """
        super().__init__(**kwargs)

        self.rows: list[Adw.PreferencesRow] = []
        self.__factory: DynamicPreferencesRowFactory = None

    @Gtk.Template.Callback()
    def on_add_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle the add button.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        if self.__factory is None:
            return
        row = self.__factory.create_row()
        self.add_row(row)

    def set_factory(self, factory: DynamicPreferencesRowFactory) -> None:
        """
        Set the factory for this group.

        Parameters:
            factory (DynamicPreferencesRowFactory): The factory to set
        """
        self.__factory = factory

    def clear_rows(self) -> None:
        """
        Clear all the rows from this group.
        """
        for row in self.rows:
            self.remove(row)
        self.rows = []
        self.empty_row.show()
        self.is_empty = True

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
            self.is_empty = len(self.rows) == 0
            self.emit('row-removed', row)
            return True
        return False

    def generate_row(self) -> Adw.PreferencesRow | None:
        """
        Generate a row.

        Returns:
            Adw.PreferencesRow | None: A row if there is a factory, None otherwise.
        """
        if self.__factory is None:
            return None
        row = self.__factory.create_row()
        self.add_row(row)
        return row

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

        if self.can_user_add:
            def row_removed(button: Gtk.Button) -> None:
                """
                Handle the row removal.

                Parameters:
                    row (KeyValueRow): The row to remove.
                    button (Gtk.Button): The button that was clicked.
                """
                self.remove_row(row)

            remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
            remove_btn.add_css_class('destructive-action')
            remove_btn.connect('clicked', row_removed)
            row.add_suffix(remove_btn)

        self.add(row)
        self.rows.append(row)
        self.is_empty = False
        self.emit('row-added', row)
        return True
