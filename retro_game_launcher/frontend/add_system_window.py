import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.widgets.directory_entry_row import DirectoryEntryRow, DirectoryEntryRowFactory
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesGroup

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/add_system_window.ui')
class AddSystemWindow(Adw.Window):
    """
    Handle the window for adding a system.
    """

    __gtype_name__ = 'AddSystemWindow'
    __gsignals__ = {
        'add_system': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    toast_overlay: Adw.ToastOverlay = Gtk.Template.Child()
    add_system_btn: Gtk.Button = Gtk.Template.Child()
    system_name_entry: Adw.EntryRow = Gtk.Template.Child()
    games_directory_group: DynamicPreferencesGroup = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        """
        Initialize the window.
        """
        super().__init__(**kwargs)
        self.add_system_btn.set_sensitive(False)
        self.games_directory_group.set_factory(DirectoryEntryRowFactory())

    @Gtk.Template.Callback()
    def on_cancel_clicked(self, button: Gtk.Button) -> None:
        """
        Handle closing the window.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.close()

    @Gtk.Template.Callback()
    def on_add_system_clicked(self, button: Gtk.Button) -> None:
        """
        Handle adding the system.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        # Create and save the config
        sc = SystemConfig(system_name=self.system_name_entry.get_text(),
                          game_directories=list(dict.fromkeys(list(filter(lambda path : os.path.isdir(path), [ row.get_text() for row in self.games_directory_group.rows ])))))
        sc.save()

        # Emit signal and close the window
        self.emit('add_system', sc.name)
        self.close()

    @Gtk.Template.Callback()
    def on_system_entry_changed(self, _: Adw.EntryRow) -> None:
        """
        Handle the system entry data changing.

        Parameters:
            _ (Adw.EntryRow): Unused
        """
        self.__update_add_btn()

    @Gtk.Template.Callback()
    def on_games_directory_row_added(self, group: DynamicPreferencesGroup, row: DirectoryEntryRow) -> None:
        def row_removed(button: Gtk.Button) -> None:
            self.games_directory_group.remove_row(row)

        def row_changed(row: DirectoryEntryRow) -> None:
            self.__update_add_btn()

        def directory_found(row: DirectoryEntryRow, path: str) -> None:
            row.set_text(path)

        row.set_title("Directory")
        row.set_transient_parent(self)
        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', row_removed)
        row.add_suffix(remove_btn)
        row.connect('changed', row_changed)
        row.connect('directory_found', directory_found)

    def __update_add_btn(self) -> None:
        system_name = self.system_name_entry.get_text()
        self.add_system_btn.set_sensitive(not SystemConfig.system_exists(system_name) and
                                          not system_name.startswith(' ') and
                                          not system_name.endswith(' ') and
                                          len(system_name) > 0 and
                                          len(self.games_directory_group.rows) > 0 and
                                          all(os.path.isdir(r.get_text()) for r in self.games_directory_group.rows))
