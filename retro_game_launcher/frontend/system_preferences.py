import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_preferences.ui')
class SystemPreferences(Adw.PreferencesWindow):
    __gtype_name__ = 'SystemPreferences'

    command_entry = Gtk.Template.Child()
    games_directory_entry = Gtk.Template.Child()
    extension_group = Gtk.Template.Child()
    empty_row = Gtk.Template.Child()
    extension_rows = []

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.command_entry.set_text(self.config.get_launch_command())
        self.games_directory_entry.set_text(self.config.get_games_dir())
        extensions = self.config.get_extensions()
        if len(extensions) == 0:
            self.empty_row.show()
        else:
            self.empty_row.hide()
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
    def command_changed(self, *args):
        self.config.set_launch_command(args[0].get_text())
        self.config.save()

    @Gtk.Template.Callback()
    def games_directory_changed(self, *args):
        dir = args[0].get_text()
        if os.path.isdir(dir):
            self.config.set_games_dir(dir)
            self.config.save()

    @Gtk.Template.Callback()
    def choose_games_directory_clicked(self, *args):
        self.games_directory_chooser.show()

    @Gtk.Template.Callback()
    def add_extension_clicked(self, *args):
        ext = self.config.get_extensions()
        ext.append('')
        self.config.set_extensions(ext)
        self.config.save()
        self.add_extension_row()

    def add_extension_row(self, extension=''):
        row = Adw.EntryRow(title="File extension")
        row.set_text(extension)
        row.connect('changed', self.extension_row_changed)
        remove_btn = Gtk.Button(valign=Gtk.Align.CENTER, icon_name='user-trash-symbolic')
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', self.remove_extension_row_clicked)
        row.add_suffix(remove_btn)
        self.extension_rows.append(row)
        self.extension_group.add(row)

    def extension_row_changed(self, *args):
        self.save_extensions()

    def remove_extension_row_clicked(self, *args):
        row = args[0].get_parent().get_parent().get_parent()
        if row in self.extension_rows:
            self.extension_group.remove(row)
            self.extension_rows.remove(row)
            self.save_extensions()

    def save_extensions(self):
        self.config.set_extensions([ row.get_text() for row in self.extension_rows ])
        self.config.save()

    def games_directory_response(self, *args):
        if args[1] == Gtk.ResponseType.ACCEPT:
            file = self.games_directory_chooser.get_file()
            path = file.get_path()
            if path is not None:
                self.games_directory_entry.set_text(path)
