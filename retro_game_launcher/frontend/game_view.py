import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, GdkPixbuf, Gio, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.system import SystemConfig
from retro_game_launcher.backend.game import Game

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/game_view.ui')
class GameView(Gtk.Box):
    __gtype_name__ = 'GameView'

    factory = GObject.Property(type=Gtk.SignalListItemFactory, default=None)
    games = GObject.Property(type=Gio.ListStore, default=None)
    has_games = GObject.Property(type=bool, default=False)
    none_title = GObject.Property(type=str, default="No games found")
    none_description = GObject.Property(type=str, default="Add games!")
    none_icon_name = GObject.Property(type=str, default="applications-games-symbolic")

    none_found = Gtk.Template.Child()
    found = Gtk.Template.Child()
    model_view = Gtk.Template.Child()

    system_config = None

    def __init__(self, **kwargs):
        self.factory = Gtk.SignalListItemFactory()
        self.games = Gio.ListStore.new(Game)

        super().__init__(**kwargs)

        self.factory.connect('bind', self.on_factory_bind)

    def set_system_config(self, system_config):
        self.system_config = system_config

    def set_none_title(self, value):
        self.none_title = value

    def set_none_description(self, value):
        self.none_description = value

    def set_none_icon_name(self, value):
        self.none_icon_name = value

    def on_factory_bind(self, widget, item):
        if self.system_config is None:
            return

        thumbnail_size = self.system_config.image_thumbnail_size

        data = item.get_item()

        builder = Gtk.Builder.new_from_resource('/com/charlieqle/RetroGameLauncher/ui/game_item.ui')
        game_item = builder.get_object('game_item')
        thumbnail_box = builder.get_object('thumbnail_box')
        thumbnail_img = builder.get_object('thumbnail_img')
        no_cover_box = builder.get_object('no_cover_box')
        label_no_cover = builder.get_object('label_no_cover')
        game_name_label = builder.get_object('game_name_label')
        play_game_btn = builder.get_object('play_game_btn')
        thumbnail_path = data.get_thumbnail_path()
        if thumbnail_path is None:
            thumbnail_img.hide()
        else:
            no_cover_box.hide()
            thumbnail_img.set_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail_path, thumbnail_size[0], thumbnail_size[1]))

        game_name_label.set_text(data.game_name)

        play_game_btn.connect('clicked', lambda *args : data.run())

        thumbnail_box.set_size_request(thumbnail_size[0], thumbnail_size[1])

        item.set_activatable(False)
        item.set_child(game_item)

    def clear_games(self):
        self.games.remove_all()
        self.has_games = False

    def add_game(self, game: Game):
        self.games.append(game)
        self.has_games = True

    def insert_game(self, position: int, game: Game):
        self.games.insert(position, game)

    def __len__(self) -> int:
        return len(self.games)

