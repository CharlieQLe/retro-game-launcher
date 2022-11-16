import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.system import SystemConfig
from retro_game_launcher.frontend.system_preferences import SystemPreferences

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_box.ui')
class SystemBox(Gtk.Box):
    __gtype_name__ = 'SystemBox'
    __gsignals__ = {
        'closed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    header = Gtk.Template.Child()
    go_back_btn = Gtk.Template.Child()
    refresh_btn = Gtk.Template.Child()

    def __init__(self, system_name, application, window, **kwargs):
        super().__init__(**kwargs)
        self.system_name = system_name
        self.application = application
        self.window = window
        self.header.set_title_widget(Adw.WindowTitle(title=system_name))
        self.system_config = SystemConfig.load(system_name)

        # TODO: Display games

        self.application.create_action('manage_system', self.manage_system)
        self.application.create_action('delete_system', self.delete_system)

    @Gtk.Template.Callback()
    def back_clicked(self, *args):
        self.application.remove_action('app.manage_system')
        self.application.remove_action('app.delete_system')
        self.emit('closed')

    @Gtk.Template.Callback()
    def refresh_clicked(self, *args):
        pass

    def manage_system(self, widget, _):
        pref = SystemPreferences(config=self.system_config)
        pref.set_transient_for(self.window)
        pref.present()

    def delete_system(self, widget, _):
        pass
