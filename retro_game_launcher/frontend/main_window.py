import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from retro_game_launcher.backend.system import SystemConfig
from retro_game_launcher.frontend.add_system_window import AddSystemWindow
from retro_game_launcher.frontend.system_row import SystemRow
from retro_game_launcher.frontend.system_box import SystemBox

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    toast_overlay = Gtk.Template.Child()
    systems_found = Gtk.Template.Child()
    no_systems_found = Gtk.Template.Child()
    system_list = Gtk.Template.Child()
    leaflet = Gtk.Template.Child()
    home = Gtk.Template.Child()
    system_box_map = {}
    system_rows = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._reload_systems()

    @Gtk.Template.Callback()
    def add_system_clicked(self, *args):
        win = AddSystemWindow(application=self.get_application(), transient_for=self)
        win.connect('add_system', self._on_system_added)
        win.show()

    def _reload_systems(self):
        # Remove existing rows
        for row in self.system_rows:
            self.system_list.remove(row)
        self.system_rows = []

        system_names = SystemConfig.get_system_names()
        if len(system_names) > 0:
            self.no_systems_found.hide()
            self.systems_found.show()
            for system_name in system_names:
                row = SystemRow(system_name)
                row.connect('open_system', self._open_system)
                self.system_list.insert(row, -1)
                self.system_rows.append(row)
        else:
            self.systems_found.hide()
            self.no_systems_found.show()

    def _on_system_added(self, _, system_name):
        self._reload_systems()

    def _open_system(self, *args):
        self._open_system_page(args[0].system_name)

    def _open_system_page(self, system_name):
        if system_name not in self.system_box_map:
            box = SystemBox(system_name, self.get_application())
            box.connect('closed', self._close_system_page)
            self.leaflet.append(box)
            self.system_box_map[system_name] = box
        self.leaflet.set_visible_child(self.system_box_map[system_name])

    def _close_system_page(self, *args):
        self.leaflet.set_visible_child(self.home)
