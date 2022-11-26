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
    preset_model: Gtk.StringList = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        """
        Initialize the window.
        """
        super().__init__(**kwargs)
        self.add_system_btn.set_sensitive(False)
        self.games_directory_group.set_factory(DirectoryEntryRowFactory())

        self.__presets = []
        self.__selected_preset = 0
        added_presets = set()
        for preset_path in utility.get_presets():
            preset_name = os.path.basename(preset_path)[:-5]
            if preset_name in added_presets:
                continue
            sc = SystemConfig.load_from_path(preset_name, preset_path)
            if sc is None:
                continue
            self.preset_model.append(preset_name)
            added_presets.add(preset_name)
            self.__presets.append(sc)

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
        sc = SystemConfig()
        sc.name = self.system_name_entry.get_text()
        sc.config_path = SystemConfig.generate_config_path(sc.name)
        sc.game_directories = list(dict.fromkeys(list(filter(lambda path : os.path.isdir(path), [ row.get_text() for row in self.games_directory_group.rows ]))))
        if self.__selected_preset > 0:
            preset = self.__presets[self.__selected_preset - 1]
            sc.extensions = preset.extensions
            sc.emulator_command = preset.emulator_command
            sc.launch_command = preset.launch_command
            sc.launch_var = preset.launch_var
            sc.image_thumbnail_size = preset.image_thumbnail_size
        sc.save()

        # Emit signal and close the window
        self.emit('add_system', sc.name)
        self.close()

    @Gtk.Template.Callback()
    def on_preset_dropdown_notify_selected(self, dropdown, selected):
        self.__selected_preset = dropdown.get_selected()
        if self.__selected_preset == 0:
            self.system_name_entry.set_text('')
        else:
            preset = self.__presets[self.__selected_preset-1]
            self.system_name_entry.set_text(preset.name)

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
        def row_changed(row: DirectoryEntryRow) -> None:
            self.__update_add_btn()

        def directory_found(row: DirectoryEntryRow, path: str) -> None:
            row.set_text(path)

        row.set_title("Directory")
        row.set_transient_parent(self)
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
