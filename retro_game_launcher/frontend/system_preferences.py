import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from retro_game_launcher.backend.system import SystemConfig

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_preferences.ui')
class SystemPreferences(Adw.PreferencesWindow):
    __gtype_name__ = 'SystemPreferences'

    launch_command_entry = Gtk.Template.Child()
    emulator_command_entry = Gtk.Template.Child()
    games_directory_entry = Gtk.Template.Child()
    thumbnail_width_spbtn = Gtk.Template.Child()
    thumbnail_height_spbtn = Gtk.Template.Child()
    extension_group = Gtk.Template.Child()
    empty_extension_row = Gtk.Template.Child()
    extension_rows = []

    def __init__(self, config: SystemConfig, **kwargs):
        super().__init__(**kwargs)
        self.config = config

        thumbnail_size = self.config.image_thumbnail_size
        self.thumbnail_width_spbtn.set_value(thumbnail_size[0])
        self.thumbnail_height_spbtn.set_value(thumbnail_size[1])

        self.launch_command_entry.set_text(' '.join(self.config.launch_command))
        self.emulator_command_entry.set_text(' '.join(self.config.emulator_command))
        self.games_directory_entry.set_text(self.config.games_directory)
        extensions = self.config.extensions
        if len(extensions) == 0:
            self.empty_extension_row.show()
        else:
            self.empty_extension_row.hide()
            for extension in extensions:
                self.add_extension_row(extension)
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

    @Gtk.Template.Callback()
    def on_add_extension_clicked(self, *args):
        extensions = self.config.extensions
        extensions.append('')
        self.config.extensions = extensions
        self.config.save()
        self.add_extension_row()
        self.empty_extension_row.hide()

    def add_extension_row(self, extension=''):
        row = Adw.EntryRow(title="File extension")
        row.set_text(extension)
        row.connect('changed', self.extension_row_changed)
        self.extension_rows.append(row)
        self.extension_group.add(row)
        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', self.remove_extension_row_clicked)
        row.add_suffix(remove_btn)

    def extension_row_changed(self, *args):
        self.save_extensions()

    def remove_extension_row_clicked(self, *args):
        row = args[0].get_parent().get_parent().get_parent()
        self.extension_group.remove(row)
        self.extension_rows.remove(row)
        self.save_extensions()
        if len(self.extension_rows) == 0:
            self.empty_extension_row.show()

    def save_extensions(self):
        self.config.extensions = [ row.get_text() for row in self.extension_rows ]
        self.config.save()

    def games_directory_response(self, *args):
        if args[1] == Gtk.ResponseType.ACCEPT:
            file = self.games_directory_chooser.get_file()
            path = file.get_path()
            if path is not None:
                self.games_directory_entry.set_text(path)
