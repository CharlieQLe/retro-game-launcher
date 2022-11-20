import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesGroup, DynamicPreferencesRowFactory

class KeyValueRow(Adw.ActionRow):
    __gtype_name__ = 'KeyValueRow'
    __gsignals__ = {
        'key_value_changed': (GObject.SIGNAL_RUN_FIRST, None, (str,str))
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = Gtk.Box(hexpand=True, valign=Gtk.Align.CENTER)
        box.add_css_class('linked')
        self.key_entry = Gtk.Entry(placeholder_text=_('key'), hexpand=True, valign=Gtk.Align.CENTER)
        self.key_entry.connect('changed', self.key_value_changed)
        self.value_entry = Gtk.Entry(placeholder_text=_('value'), hexpand=True, valign=Gtk.Align.CENTER)
        self.value_entry.connect('changed', self.key_value_changed)
        box.append(self.key_entry)
        box.append(self.value_entry)
        self.add_prefix(box)

    @property
    def key(self) -> str:
        return self.key_entry.get_text()

    @key.setter
    def key(self, key: str):
        self.key_entry.set_text(key)

    @property
    def value(self) -> str:
        return self.value_entry.get_text()

    @value.setter
    def value(self, value: str):
        self.value_entry.set_text(value)

    def key_value_changed(self, *args):
        self.emit('key_value_changed', self.key_entry.get_text(), self.value_entry.get_text())

class LaunchVarRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> Adw.PreferencesRow:
        return KeyValueRow()

class ExtensionRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> Adw.PreferencesRow:
        return Adw.EntryRow(title="File extension")

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_preferences.ui')
class SystemPreferences(Adw.PreferencesWindow):
    __gtype_name__ = 'SystemPreferences'

    launch_command_entry = Gtk.Template.Child()
    emulator_command_entry = Gtk.Template.Child()
    launch_var_group = Gtk.Template.Child()
    games_directory_entry = Gtk.Template.Child()
    thumbnail_width_spbtn = Gtk.Template.Child()
    thumbnail_height_spbtn = Gtk.Template.Child()
    extension_group = Gtk.Template.Child()

    def __init__(self, config: SystemConfig, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        thumbnail_size = self.config.image_thumbnail_size
        self.thumbnail_width_spbtn.set_value(thumbnail_size[0])
        self.thumbnail_height_spbtn.set_value(thumbnail_size[1])
        self.launch_command_entry.set_text(' '.join(self.config.launch_command))
        self.emulator_command_entry.set_text(' '.join(self.config.emulator_command))
        self.games_directory_entry.set_text(self.config.games_directory)

        self.launch_var_group.set_factory(LaunchVarRowFactory())
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
            row = Adw.EntryRow(title="File extension")
            row.set_text(extension)
            self.update_extension_row(row)
            self.extension_group.add_row(row)

        self.games_directory_chooser = Gtk.FileChooserNative(
            title='Select a folder',
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            modal=True,
            select_multiple=False,
            accept_label='Select',
            cancel_label='Cancel',
            transient_for=self)
        self.games_directory_chooser.connect('response', self.games_directory_response)

    @Gtk.Template.Callback()
    def on_launch_command_entry_changed(self, *args):
        launch_str = args[0].get_text()
        self.config.launch_command = launch_str.split(' ')
        self.config.save()

    @Gtk.Template.Callback()
    def on_emulator_command_entry_changed(self, *args):
        emulator_str = args[0].get_text()
        self.config.emulator_command = emulator_str.split(' ')
        self.config.save()

    @Gtk.Template.Callback()
    def on_games_directory_entry_changed(self, *args):
        dir = args[0].get_text()
        if os.path.isdir(dir):
            self.config.games_directory = dir
            self.config.save()

    @Gtk.Template.Callback()
    def on_choose_games_directory_clicked(self, *args):
        self.games_directory_chooser.show()

    @Gtk.Template.Callback()
    def on_thumbnail_size_spbtn_value_changed(self, *args):
        self.config.image_thumbnail_size = (self.thumbnail_width_spbtn.get_value(), self.thumbnail_height_spbtn.get_value())
        self.config.save()

    ### LAUNCH

    def on_launch_var_row_added(self, _, row):
        self.update_launch_var_row(row)

    def update_launch_var_row(self, row):
        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', self.remove_launch_var_row_clicked)
        row.add_suffix(remove_btn)
        row.connect('key_value_changed', self.launch_var_row_changed)

    def launch_var_row_changed(self, *args):
        self.save_launch_variables()

    def remove_launch_var_row_clicked(self, *args):
        self.launch_var_group.remove_row(args[0].get_parent().get_parent().get_parent())
        self.save_launch_variables()

    def save_launch_variables(self):
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

    def on_extension_row_added(self, _, row):
        extensions = self.config.extensions
        extensions.append('')
        self.config.extensions = extensions
        self.config.save()
        self.update_extension_row(row)

    def update_extension_row(self, row):
        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', self.remove_extension_row_clicked)
        row.add_suffix(remove_btn)
        row.connect('changed', self.extension_row_changed)

    def extension_row_changed(self, *args):
        self.save_extensions()

    def remove_extension_row_clicked(self, *args):
        self.extension_group.remove_row(args[0].get_parent().get_parent().get_parent())
        self.save_extensions()

    def save_extensions(self):
        self.config.extensions = [ row.get_text() for row in self.extension_group.rows ]
        self.config.save()

    ###

    def games_directory_response(self, *args):
        if args[1] == Gtk.ResponseType.ACCEPT:
            file = self.games_directory_chooser.get_file()
            path = file.get_path()
            if path is not None:
                self.games_directory_entry.set_text(path)
