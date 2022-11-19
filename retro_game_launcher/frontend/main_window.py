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
    system_map = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Remove existing systems
        for system_name in self.system_map:
            box = self.system_map[system_name]['box']
            row = self.system_map[system_name]['row']
            if box is not None:
                self.leaflet.remove(box)
            if row is not None:
                self.system_list.remove(row)
        self.system_map = {}

        system_names = SystemConfig.get_system_names()
        if len(system_names) > 0:
            self.no_systems_found.hide()
            self.systems_found.show()
            for system_name in system_names:
                self.add_system(system_name)
        else:
            self.systems_found.hide()
            self.no_systems_found.show()

    @Gtk.Template.Callback()
    def on_add_system_clicked(self, *args):
        win = AddSystemWindow(application=self.get_application(), transient_for=self)
        win.connect('add_system', self._on_system_added)
        win.show()

    def add_system(self, system_name):
        row = SystemRow(system_name)
        row.connect('open_system', self._open_system)
        self.system_list.insert(row, -1)
        self.system_map[system_name] = {
            'box': None,
            'row': row
        }

    def _on_system_added(self, _, system_name):
        self.no_systems_found.hide()
        self.systems_found.show()
        self.add_system(system_name)

    def _on_system_deleted(self, _, system_name):
        if system_name in self.system_map:
            box = self.system_map[system_name]['box']
            row = self.system_map[system_name]['row']
            self.leaflet.remove(box)
            self.system_list.remove(row)
            self.system_map.pop(system_name)
            SystemConfig.delete(system_name)
            if len(SystemConfig.get_system_names()) == 0:
                self.no_systems_found.show()
                self.systems_found.hide()

    def _open_system(self, *args):
        self._open_system_page(args[0].system_name)

    def _open_system_page(self, system_name):
        if self.system_map[system_name]['box'] is None:
            box = SystemBox(system_name, self.get_application(), self)
            box.connect('closed', self._close_system_page)
            box.connect('deleted', self._on_system_deleted)
            self.leaflet.append(box)
            self.system_map[system_name]['box'] = box
        self.leaflet.set_visible_child(self.system_map[system_name]['box'])

    def _close_system_page(self, *args):
        self.leaflet.set_visible_child(self.home)
