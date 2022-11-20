import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_row.ui')
class SystemRow(Adw.ActionRow):
    __gtype_name__ = 'SystemRow'
    __gsignals__ = {
        'open_system': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, system_name: str, **kwargs):
        kwargs['title'] = system_name
        super().__init__(**kwargs)
        self.system_name = system_name

    @Gtk.Template.Callback()
    def open_clicked(self, *args):
        self.emit('open_system')
