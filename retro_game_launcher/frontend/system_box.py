import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gdk, Gio, GLib, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.system import SystemConfig
from retro_game_launcher.backend.game import Game
from retro_game_launcher.frontend.system_preferences import SystemPreferences

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/system_box.ui')
class SystemBox(Gtk.Box):
    __gtype_name__ = 'SystemBox'
    __gsignals__ = {
        'closed': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'deleted': (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }
    __gproperties__ = {
        'games': (Gio.ListStore, 'games', 'Store all found games', GObject.ParamFlags.READWRITE)
    }

    header = Gtk.Template.Child()
    go_back_btn = Gtk.Template.Child()
    refresh_btn = Gtk.Template.Child()
    no_games_found = Gtk.Template.Child()
    games_found = Gtk.Template.Child()
    game_view = Gtk.Template.Child()

    def __init__(self, system_name, application, window, **kwargs):
        self.games = Gio.ListStore.new(Game)

        super().__init__(**kwargs)

        self.factory = Gtk.SignalListItemFactory()
        self.factory.connect('setup', self.on_factory_setup)
        self.factory.connect('bind', self.on_factory_bind)
        self.factory.connect('unbind', self.on_factory_unbind)
        self.factory.connect('teardown', self.on_factory_teardown)
        self.game_view.set_factory(self.factory)

        self.system_name = system_name
        self.application = application
        self.window = window
        self.header.set_title_widget(Adw.WindowTitle(title=system_name))
        self.system_config = SystemConfig.load(system_name)

        self.application.create_action('manage_system', self.manage_system)
        self.application.create_action('delete_system', self.delete_system)

        self.delete_dialog = Adw.MessageDialog(
            modal=True,
            heading='Delete %s?' % system_name,
            body='This cannot be undone! Are you sure you want to delete %s?' % system_name)
        self.delete_dialog.add_response('cancel', _('_Cancel'))
        self.delete_dialog.add_response('delete', _('_Delete'))
        self.delete_dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        self.delete_dialog.set_transient_for(window)
        self.delete_dialog.connect('response', self.delete_response)

        self.reload_view()

    def on_factory_setup(self, widget, item):
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_hexpand(True)
        label.set_margin_start(10)
        label.set_margin_end(10)
        label.set_margin_top(10)
        label.set_margin_bottom(10)
        item.set_child(label)

    def on_factory_bind(self, widget, item):
        label = item.get_child()
        data = item.get_item()
        label.set_text(data.game_name)
        item.set_child(label)

    def on_factory_unbind(self, widget, item):
        pass

    def on_factory_teardown(self, widget, item):
        pass

    def do_get_property(self, prop):
        if prop.name == 'games':
            return self.games
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_set_property(self, prop, value):
        if prop.name == 'games':
            self.games = value
        else:
            raise AttributeError('unknown property %s' % prop.name)

    @Gtk.Template.Callback()
    def back_clicked(self, *args):
        self.on_closed()

    @Gtk.Template.Callback()
    def refresh_clicked(self, *args):
        self.reload_view()

    @Gtk.Template.Callback()
    def open_games_clicked(self, *args):
        Gtk.show_uri(self.window, GLib.filename_to_uri(self.system_config.get_games_dir()), Gdk.CURRENT_TIME)

    def on_closed(self):
        self.application.remove_action('app.manage_system')
        self.application.remove_action('app.delete_system')
        self.emit('closed')

    def manage_system(self, widget, _):
        pref = SystemPreferences(config=self.system_config)
        pref.set_transient_for(self.window)
        pref.present()

    def delete_system(self, widget, _):
        self.delete_dialog.show()

    def delete_response(self, *args):
        if args[1] == 'delete':
            self.on_closed()
            self.emit('deleted', self.system_name)
        else:
            self.delete_dialog.hide()

    def reload_view(self):
        self.games.remove_all()
        game_subfolders = self.system_config.get_game_subfolders()
        if len(game_subfolders) == 0:
            self.no_games_found.show()
            self.games_found.hide()
        else:
            self.no_games_found.hide()
            self.games_found.show()
            extensions = self.system_config.get_extensions()
            for game_subfolder in game_subfolders:
                game_subfolder_dir = os.path.join(self.system_config.get_games_dir(), game_subfolder)
                game_subfolder_contents = os.listdir(game_subfolder_dir)
                game_file_name = next(filter(lambda file_name : any(file_name.endswith(ext) for ext in extensions), game_subfolder_contents))
                if game_file_name is None:
                    continue
                game = Game(game_subfolder, game_subfolder_dir, game_file_name, self.system_config)
                self.games.append(game)
