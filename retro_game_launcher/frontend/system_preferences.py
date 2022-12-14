import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesGroup, DynamicPreferencesRowFactory
from retro_game_launcher.frontend.widgets.extension_row import ExtensionRow, ExtensionRowFactory
from retro_game_launcher.frontend.widgets.directory_entry_row import DirectoryEntryRow, DirectoryEntryRowFactory

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_preferences.ui')
class SystemPreferences(Adw.PreferencesWindow):
    """
    Handle system preferences.
    """

    __gtype_name__ = 'SystemPreferences'

    launch_command_entry = Gtk.Template.Child()
    emulator_command_entry = Gtk.Template.Child()
    games_directory_group = Gtk.Template.Child()
    thumbnail_width_spbtn = Gtk.Template.Child()
    thumbnail_height_spbtn = Gtk.Template.Child()
    extension_group = Gtk.Template.Child()

    def __init__(self, config: SystemConfig) -> None:
        """
        Initialize the preferences.

        Parameters:
            config (SystemConfig): The config for the system.
        """
        super().__init__()

        self.config = config
        thumbnail_size = self.config.image_thumbnail_size
        self.thumbnail_width_spbtn.set_value(thumbnail_size[0])
        self.thumbnail_height_spbtn.set_value(thumbnail_size[1])
        self.launch_command_entry.set_text(self.config.launch_command)
        self.emulator_command_entry.set_text(self.config.emulator_command)
        self.games_directory_group.set_factory(DirectoryEntryRowFactory())
        self.extension_group.set_factory(ExtensionRowFactory())

        for game_directory in self.config.game_directories:
            self.games_directory_group.generate_row().set_text(game_directory)

        for extension in self.config.extensions:
            self.extension_group.generate_row().set_text(extension)

    @Gtk.Template.Callback()
    def on_launch_command_entry_changed(self, row: Adw.EntryRow) -> None:
        """
        Handle the launch command changing.

        Parameters:
            row (Adw.EntryRow): The row that was changed.
        """
        self.config.launch_command = row.get_text()
        self.config.save()

    @Gtk.Template.Callback()
    def on_emulator_command_entry_changed(self, row: Adw.EntryRow) -> None:
        """
        Handle the emulator command changing.

        Parameters:
            row (Adw.EntryRow): The row that was changed.
        """
        self.config.emulator_command = row.get_text()
        self.config.save()

    @Gtk.Template.Callback()
    def on_thumbnail_size_spbtn_value_changed(self, _: Gtk.SpinButton) -> None:
        """
        Handle changing the thumbnail size.

        Parameters:
            _ (Gtk.SpinButton): Unused
        """
        self.config.image_thumbnail_size = (self.thumbnail_width_spbtn.get_value(), self.thumbnail_height_spbtn.get_value())
        self.config.save()

    ### GAME DIRECTORIES

    @Gtk.Template.Callback()
    def on_games_directory_row_added(self, group: DynamicPreferencesGroup, row: DirectoryEntryRow) -> None:
        def row_changed(row: DirectoryEntryRow) -> None:
            self.save_game_directories()

        def directory_found(row: DirectoryEntryRow, path: str) -> None:
            row.set_text(path)

        row.set_transient_parent(self)
        row.connect('changed', row_changed)
        row.connect('directory_found', directory_found)

    @Gtk.Template.Callback()
    def on_games_directory_row_removed(self, group: DynamicPreferencesGroup, row: DirectoryEntryRow) -> None:
        self.save_game_directories()

    def save_game_directories(self) -> None:
        self.config.game_directories = [ row.get_text() for row in self.games_directory_group.rows ]
        self.config.save()

    ### EXTENSIONS

    @Gtk.Template.Callback()
    def on_extension_row_added(self, group: DynamicPreferencesGroup, row: ExtensionRow) -> None:
        """
        Handle adding an extension row.

        Parameters:
            group (DynamicPreferencesGroup): The group that emitted this signal.
            row (ExtensionRow): The row that was added.
        """

        def row_changed(row: ExtensionRow) -> None:
            """
            Handle the row changing.

            Parameters:
                row (ExtensionRow): The row that emitted the signal.
            """
            self.save_extensions()

        row.connect('changed', row_changed)

    @Gtk.Template.Callback()
    def on_extension_row_removed(self, group: DynamicPreferencesGroup, row: ExtensionRow) -> None:
        self.save_extensions()

    def save_extensions(self) -> None:
        """
        Save the extensions.
        """
        self.config.extensions = [ row.get_text() for row in self.extension_group.rows ]
        self.config.save()
