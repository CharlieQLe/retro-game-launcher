import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig

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
    games_directory_entry: Adw.EntryRow = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        """
        Initialize the window.
        """
        super().__init__(**kwargs)
        self.add_system_btn.set_sensitive(False)

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

        # Get the entry data
        system_name = self.system_name_entry.get_text()
        games_directory = self.games_directory_entry.get_text()

        # Create and save the config
        sc = SystemConfig(system_name, games_directory)
        sc.save()

        # Emit signal and close the window
        self.emit('add_system', system_name)
        self.close()

    @Gtk.Template.Callback()
    def on_system_entry_changed(self, _: Adw.EntryRow) -> None:
        """
        Handle the system entry data changing.

        Parameters:
            _ (Adw.EntryRow): Unused
        """
        system_name = self.system_name_entry.get_text()
        games_directory = self.games_directory_entry.get_text()

        # Check if any of the parameters fail. If so, set sensitive to false
        self.add_system_btn.set_sensitive(
            not SystemConfig.system_exists(system_name) and
            not system_name.startswith(' ') and
            not system_name.endswith(' ') and
            len(system_name) > 0 and
            os.path.isdir(games_directory))

    @Gtk.Template.Callback()
    def on_games_directory_chooser_clicked(self, button: Gtk.Button) -> None:
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

        file_chooser = Gtk.FileChooserNative(title='Select a folder',
                                             action=Gtk.FileChooserAction.SELECT_FOLDER,
                                             modal=True,
                                             select_multiple=False,
                                             accept_label='Select',
                                             cancel_label='Cancel',
                                             transient_for=self)
        file_chooser.connect('response', file_chooser_response)
        file_chooser.show()
