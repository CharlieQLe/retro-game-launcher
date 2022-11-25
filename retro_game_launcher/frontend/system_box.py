import os
import gi
import subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gdk, GdkPixbuf, Gio, GLib, Gtk, GObject
import retro_game_launcher.backend.constants as constants
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.game import Game
from retro_game_launcher.frontend.system_preferences import SystemPreferences
from retro_game_launcher.frontend.game_view import GameView

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_box.ui')
class SystemBox(Gtk.Box):
    """
    The view for a system.

    Attributes:
        system_name (str): The name of the system.
        window (Adw.ApplicationWindow): The window this view is attached to.
    """
    __gtype_name__ = 'SystemBox'
    __gsignals__ = {
        'closed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'deleted': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    system_name: str = GObject.Property(type=str, default='')

    game_view: GameView = Gtk.Template.Child()
    pop_menu: Gtk.Popover = Gtk.Template.Child()

    def __init__(self, system_name: str, window: Adw.ApplicationWindow, **kwargs) -> None:
        """
        Initialize the system view.

        Parameters:
            system_name (str): The name of the system
            window (Adw.ApplicationWindow): The main window
        """
        super().__init__(**kwargs)

        # Set the properties
        self.system_name = system_name
        self.window = window

        self.system_config = SystemConfig.load(system_name)
        self.game_view.set_system_config(self.system_config)

        self.reload_game_view()

    @Gtk.Template.Callback()
    def on_go_back_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle going back to the main window.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.emit('closed')

    @Gtk.Template.Callback()
    def on_refresh_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle refreshing the game view.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.reload_game_view()

    @Gtk.Template.Callback()
    def on_open_emu_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the emulator.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        subprocess.Popen(self.system_config.get_substituted_emulator_command())

    @Gtk.Template.Callback()
    def on_manage_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle showing the preferences for this system.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        # Hide the menu
        self.pop_menu.popdown()

        # Create the preferences and show it
        pref = SystemPreferences(config=self.system_config)
        pref.set_transient_for(self.window)
        pref.present()

    @Gtk.Template.Callback()
    def on_delete_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle deleting the system.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """

        def delete_response(dialog: Adw.MessageDialog, response: str) -> None:
            """
            Handle the response for the deletion dialog.

            Parameters:
                dialog (Adw.MessageDialog): Dialog that emitted the response
                response (str): The response ID
            """
            if response == 'delete':
                self.emit('closed')
                self.emit('deleted', self.system_name)
            else:
                dialog.hide()

        # Hide the menu
        self.pop_menu.popdown()

        # Create the dialog and show it
        self.delete_dialog = Adw.MessageDialog(modal=True,
                                               heading='Delete %s?' % self.system_name,
                                               body='This cannot be undone! Are you sure you want to delete %s?' % self.system_name)
        self.delete_dialog.add_response('cancel', _('_Cancel'))
        self.delete_dialog.add_response('delete', _('_Delete'))
        self.delete_dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        self.delete_dialog.set_transient_for(self.window)
        self.delete_dialog.connect('response', delete_response)
        self.delete_dialog.show()

    def reload_game_view(self) -> None:
        """
        Reload the game view.
        """
        # Remove all games from the model
        self.game_view.reload(toast_overlay=self.window.toast_overlay)
