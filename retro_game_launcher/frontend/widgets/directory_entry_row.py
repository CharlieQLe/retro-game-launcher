import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.frontend.dynamic_preferences_group import DynamicPreferencesRowFactory

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/widgets/directory_entry_row.ui')
class DirectoryEntryRow(Adw.EntryRow):
    __gtype_name__ = 'DirectoryEntryRow'
    __gsignals__ = {
        'directory_found': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    def __init__(self, transient_parent, **kwargs) -> None:
        super().__init__(**kwargs)

        self.__transient_parent = transient_parent

    @Gtk.Template.Callback()
    def on_file_chooser_btn_clicked(self, button: Gtk.Button) -> None:
        def file_chooser_response(file_chooser: Gtk.FileChooserNative, response: Gtk.ResponseType) -> None:
            if response == Gtk.ResponseType.ACCEPT:
                file = file_chooser.get_file()
                path = file.get_path()
                if path is not None:
                    self.emit('directory_found', path)

        file_chooser = Gtk.FileChooserNative(title='Select a folder',
                                             action=Gtk.FileChooserAction.SELECT_FOLDER,
                                             modal=True,
                                             select_multiple=False,
                                             accept_label='Select',
                                             cancel_label='Cancel',
                                             transient_for=self.__transient_parent)
        file_chooser.connect('response', file_chooser_response)
        file_chooser.show()

class DirectoryEntryRowFactory(DynamicPreferencesRowFactory):
    def create_row(self) -> Adw.PreferencesRow:
        return DirectoryEntryRow()
