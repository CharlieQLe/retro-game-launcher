import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GObject

class DynamicPreferencesRowFactory:
    def create_row(self) -> Adw.PreferencesRow:
        raise NotImplementedError()

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/dynamic_preferences_group.ui')
class DynamicPreferencesGroup(Adw.PreferencesGroup):
    __gtype_name__ = 'DynamicPreferencesGroup'
    __gsignals__ = {
        'row_added': (GObject.SIGNAL_RUN_FIRST, None, (Adw.PreferencesRow,))
    }
    __gproperties__ = {
        'add-btn-icon-name': (str, 'add button icon name', 'add button icon name', '', GObject.PARAM_READWRITE),
        'add-btn-text': (str, 'add button text', 'add button text', '', GObject.PARAM_READWRITE),
        'empty-row-title': (str, 'empty row title', 'empty row title', '', GObject.PARAM_READWRITE)
    }

    empty_row = Gtk.Template.Child()

    add_btn_icon_name = ''
    add_btn_text = ''
    empty_row_title = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = []
        self.factory = None

    def do_get_property(self, prop):
        attr = prop.name.replace('-', '_')
        if attr in dir(self):
            return getattr(self, attr)
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop, value):
        attr = prop.name.replace('-', '_')
        if attr in dir(self):
            setattr(self, attr, value)
        else:
            raise AttributeError('unknown property %s' % prop.name)

    @Gtk.Template.Callback()
    def on_add_clicked(self, *args):
        if self.factory is None:
            return None
        row = self.factory.create_row()
        self.add_row(row)
        self.emit('row_added', row)

    def set_factory(self, factory):
        self.factory = factory

    def clear_rows(self):
        for row in self.rows:
            self.remove(row)
        self.rows = []
        self.empty_row.show()

    def remove_row(self, row) -> bool:
        if row in self.rows:
            self.remove(row)
            self.rows.remove(row)
            if len(self.rows) > 0:
                self.empty_row.hide()
            else:
                self.empty_row.show()
            return True
        return False

    def add_row(self, row: Adw.PreferencesRow):
        self.add(row)
        self.rows.append(row)
        self.empty_row.hide()
