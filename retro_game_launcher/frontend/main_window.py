import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.add_system_window import AddSystemWindow
from retro_game_launcher.frontend.system_box import SystemBox
from retro_game_launcher.frontend.preferences import Preferences

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_row.ui')
class SystemRow(Adw.ActionRow):
    """
    Handles the system row

    Attributes:
        system_name (str): The name of the system this row is for.
    """
    __gtype_name__ = 'SystemRow'
    __gsignals__ = {
        'open_system': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, system_name: str) -> None:
        """
        Initializes the system row.

        Parameters:
            system_name (str): The name of the system.
        """
        super().__init__(title=system_name)
        self.system_name = system_name

    @Gtk.Template.Callback()
    def open_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the system.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.emit('open_system')

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    """
    The main window of the application.
    """
    __gtype_name__ = 'MainWindow'

    has_systems = GObject.Property(type=bool, default=False)

    toast_overlay = Gtk.Template.Child()
    systems_found = Gtk.Template.Child()
    no_systems_found = Gtk.Template.Child()
    system_list = Gtk.Template.Child()
    leaflet = Gtk.Template.Child()
    home = Gtk.Template.Child()
    pop_menu = Gtk.Template.Child()

    def __init__(self, arg_system: str | None, **kwargs) -> None:
        """
        Initialize the window.

        Parameters:
            arg_system (str | None): The name of the system to load.
        """
        super().__init__(**kwargs)

        # Populate the system map
        self.system_map = {}
        system_names = SystemConfig.get_system_names()
        self.has_systems = len(system_names) > 0
        for system_name in system_names:
            self.add_system(system_name)

        # Open the specified system
        if arg_system is not None and arg_system in system_names:
            self.__open_system_page(arg_system, only_system=True)

    @Gtk.Template.Callback()
    def on_add_system_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the add system window.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        win = AddSystemWindow(application=self.get_application(), transient_for=self)
        win.connect('add_system', self._on_system_added)
        win.show()

    @Gtk.Template.Callback()
    def on_pref_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the preferences

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.pop_menu.popdown()
        Preferences().present()

    @Gtk.Template.Callback()
    def on_about_btn_clicked(self, button: Gtk.Button) -> None:
        """
        Handle opening the about window.

        Parameters:
            button (Gtk.Button): The button that was clicked
        """
        self.pop_menu.popdown()
        Adw.AboutWindow(transient_for=self,
                        application_name='Retro Game Launcher',
                        application_icon='applications-games-symbolic',
                        developer_name='Charlie Le',
                        version='0.1.0',
                        developers=['Charlie Le'],
                        copyright='© 2022 Charlie Le').present()

    def add_system(self, system_name: str) -> None:
        """
        Add a system.

        Parameters:
            system_name (str): The name of the system to add.
        """
        row = SystemRow(system_name)
        row.connect('open_system', self.__open_system)
        self.system_list.insert(row, -1)
        self.system_map[system_name] = {
            'box': None,
            'row': row
        }

    def _on_system_added(self, _: AddSystemWindow, system_name: str) -> None:
        """
        Handle adding a system.

        Parameters:
            _ (AddSystemWindow): Unused
            system_name (str): The name of the system to add
        """
        self.has_systems = True
        self.add_system(system_name)

    def _on_system_deleted(self, _: AddSystemWindow, system_name: str) -> None:
        """
        Handle adding a system.

        Parameters:
            _ (AddSystemWindow): Unused
            system_name (str): The name of the system to remove
        """
        if system_name not in self.system_map:
            return
        self.leaflet.remove(self.system_map[system_name]['box'])
        self.system_list.remove(self.system_map[system_name]['row'])
        self.system_map.pop(system_name)
        SystemConfig.delete(system_name)
        if len(SystemConfig.get_system_names()) == 0:
            self.has_systems = False

    def __open_system(self, system_row: SystemRow) -> None:
        """
        Handle opening a system.

        Parameters:
            system_row (SystemRow): The row that emitted this signal.
        """
        self.__open_system_page(system_row.system_name)

    def __open_system_page(self, system_name: str, only_system: bool = False) -> None:
        """
        Handle opening a system page.

        Parameters:
            system_name (str): The page to open.
            only_system (bool): If true, ensure that this page is the only one open.
        """
        if self.system_map[system_name]['box'] is None:
            box = SystemBox(system_name=system_name, window=self, only_system=only_system)
            box.connect('closed', self._close_system_page)
            box.connect('deleted', self._on_system_deleted)
            self.leaflet.append(box)
            self.system_map[system_name]['box'] = box
        self.leaflet.set_visible_child(self.system_map[system_name]['box'])

    def _close_system_page(self, system_name: str) -> None:
        """
        Handle closing a system page.

        Parameters:
            system_name (str): The page to open.
        """
        self.leaflet.set_visible_child(self.home)
