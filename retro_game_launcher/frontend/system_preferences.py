import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesGroup, DynamicPreferencesRowFactory
from retro_game_launcher.frontend.widgets.extension_row import ExtensionRow, ExtensionRowFactory
from retro_game_launcher.frontend.widgets.key_value_row import KeyValueRow, KeyValueRowFactory

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_preferences.ui')
class SystemPreferences(Adw.PreferencesWindow):
    """
    Handle system preferences.
    """

    __gtype_name__ = 'SystemPreferences'

    launch_command_entry = Gtk.Template.Child()
    emulator_command_entry = Gtk.Template.Child()
    launch_var_group = Gtk.Template.Child()
    games_directory_entry = Gtk.Template.Child()
    thumbnail_width_spbtn = Gtk.Template.Child()
    thumbnail_height_spbtn = Gtk.Template.Child()
    extension_group = Gtk.Template.Child()

    def __init__(self, config: SystemConfig, transient_parent: Gtk.Widget) -> None:
        """
        Initialize the preferences.

        Parameters:
            config (SystemConfig): The config for the system.
            transient_parent (Gtk.Widget): The transient parent of this window.
        """
        super().__init__()
        self.config = config
        self.set_transient_for(transient_parent)
        thumbnail_size = self.config.image_thumbnail_size
        self.thumbnail_width_spbtn.set_value(thumbnail_size[0])
        self.thumbnail_height_spbtn.set_value(thumbnail_size[1])
        self.launch_command_entry.set_text(' '.join(self.config.launch_command))
        self.emulator_command_entry.set_text(' '.join(self.config.emulator_command))
        self.games_directory_entry.set_text(self.config.games_directory)

        self.launch_var_group.set_factory(KeyValueRowFactory())
        self.extension_group.set_factory(ExtensionRowFactory())
        self.launch_var_group.connect('row_added', self.on_launch_var_row_added)
        self.extension_group.connect('row_added', self.on_extension_row_added)

        for launch_key, launch_value in self.config.launch_var.items():
            row = KeyValueRow()
            row.key = launch_key
            row.value = ' '.join(launch_value) if launch_key.startswith('CMD_') else launch_value
            self.update_launch_var_row(row)
            self.launch_var_group.add_row(row)

        for extension in self.config.extensions:
            row = ExtensionRow()
            row.set_text(extension)
            self.update_extension_row(row)
            self.extension_group.add_row(row)

    @Gtk.Template.Callback()
    def on_launch_command_entry_changed(self, row: Adw.EntryRow) -> None:
        """
        Handle the launch command changing.

        Parameters:
            row (Adw.EntryRow): The row that was changed.
        """
        self.config.launch_command = row.get_text().split(' ')
        self.config.save()

    @Gtk.Template.Callback()
    def on_emulator_command_entry_changed(self, row: Adw.EntryRow) -> None:
        """
        Handle the emulator command changing.

        Parameters:
            row (Adw.EntryRow): The row that was changed.
        """
        self.config.emulator_command = row.get_text().split(' ')
        self.config.save()

    @Gtk.Template.Callback()
    def on_games_directory_entry_changed(self, row: Adw.EntryRow) -> None:
        """
        Handle the games directory entry changing.

        Parameters:
            row (Adw.EntryRow): The row that was changed.
        """
        dir = row.get_text()
        if os.path.isdir(dir):
            self.config.games_directory = dir
            self.config.save()

    @Gtk.Template.Callback()
    def on_choose_games_directory_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the file chooser for the games directory.

        Parameters:
            button (Gtk.Button): The button that was clicked.
        """
        def file_chooser_response(file_chooser: Gtk.FileChooserNative, response: Gtk.ResponseType) -> None:
            """
            Handle the response from the file chooser.

            Parameters:
                file_chooser (Gtk.FileChooserNative): The file chooser that emitted the response.
                response (Gtk.ResponseType): The response type.
            """
            if response == Gtk.ResponseType.ACCEPT:
                file = file_chooser.get_file()
                path = file.get_path()
                if path is not None:
                    self.games_directory_entry.set_text(path)

        file_chooser = Gtk.FileChooserNative(
            title='Select a folder',
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            modal=True,
            select_multiple=False,
            accept_label='Select',
            cancel_label='Cancel',
            transient_for=self)
        file_chooser.connect('response', file_chooser_response)
        file_chooser.show()

    @Gtk.Template.Callback()
    def on_thumbnail_size_spbtn_value_changed(self, _: Gtk.SpinButton) -> None:
        """
        Handle changing the thumbnail size.

        Parameters:
            _ (Gtk.SpinButton): Unused
        """
        self.config.image_thumbnail_size = (self.thumbnail_width_spbtn.get_value(), self.thumbnail_height_spbtn.get_value())
        self.config.save()

    ### LAUNCH

    def on_launch_var_row_added(self, group: DynamicPreferencesGroup, row: KeyValueRow) -> None:
        """
        Handle adding a command row.

        Parameters:
            group (DynamicPreferencesGroup): The parent of the row.
            row (KeyValueRow): The added row.
        """
        self.update_launch_var_row(row)

    def update_launch_var_row(self, row: KeyValueRow):
        """
        Handle updating a command row.

        Parameters:
            row (KeyValueRow): The row to update.
        """

        def row_removed(button: Gtk.Button) -> None:
            """
            Handle the row removal.

            Parameters:
                row (KeyValueRow): The row to remove.
                button (Gtk.Button): The button that was clicked.
            """
            self.launch_var_group.remove_row(row)
            self.save_launch_variables()

        def row_changed(row: KeyValueRow, key: str, value: str) -> None:
            """
            Handle the row changing.

            Parameters:
                row (KeyValueRow): The row that was changed.
                key (str): The key of the variable.
                value (str): The value for the variable.
            """
            self.save_launch_variables()

        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', row_removed)
        row.add_suffix(remove_btn)

        row.connect('key_value_changed', row_changed)

    def save_launch_variables(self) -> None:
        """
        Handle saving launch variables.
        """
        vars = {}
        for row in self.launch_var_group.rows:
            key = row.key
            value = row.value
            if key.startswith('CMD_'):
                vars[key] = value.split(' ')
            else:
                vars[key] = value
        self.config.launch_var = vars
        self.config.save()

    ### EXTENSIONS

    def on_extension_row_added(self, group: DynamicPreferencesGroup, row: ExtensionRow) -> None:
        """
        Handle adding an extension row.

        Parameters:
            group (DynamicPreferencesGroup): The group that emitted this signal.
            row (ExtensionRow): The row that was added.
        """
        extensions = self.config.extensions
        extensions.append('')
        self.config.extensions = extensions
        self.config.save()
        self.update_extension_row(row)

    def update_extension_row(self, row: ExtensionRow) -> None:
        """
        Update the extension row.

        Parameters:
            row (ExtensionRow): The row to update.
        """
        def row_removed(row: ExtensionRow, button: Gtk.Button) -> None:
            """
            Handle the row removal.

            Parameters:
                row (ExtensionRow): The row that emitted the signal.
                button (Gtk.Button): The button that was clicked.
            """
            self.extension_group.remove_row(row)
            self.save_extensions()

        def row_changed(row: ExtensionRow) -> None:
            """
            Handle the row changing.

            Parameters:
                row (ExtensionRow): The row that emitted the signal.
            """
            self.save_extensions()

        row.connect('remove_clicked', row_removed)
        row.connect('changed', row_changed)

    def save_extensions(self) -> None:
        """
        Save the extensions.
        """
        self.config.extensions = [ row.get_text() for row in self.extension_group.rows ]
        self.config.save()
