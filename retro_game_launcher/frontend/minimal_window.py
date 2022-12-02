import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from retro_game_launcher.backend.config import SystemConfig

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/minimal_window.ui')
class MinimalWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MinimalWindow'

    game_view = Gtk.Template.Child()

    def __init__(self, system_name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__system_name = system_name
        self.__system_config = SystemConfig.load(system_name)
        self.game_view.set_system_config(self.__system_config)
        self.game_view.reload()

    @Gtk.Template.Callback()
    def on_open_emu_btn_clicked(self, button):
        self.__system_config.run_emulator_command()
