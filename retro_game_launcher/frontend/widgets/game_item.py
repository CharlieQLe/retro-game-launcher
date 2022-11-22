import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import GdkPixbuf, Gtk, GObject
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.game import Game

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/widgets/game_item.ui')
class GameItem(Gtk.Box):
    __gtype_name__ = 'GameItem'

    thumbnail_box = Gtk.Template.Child()
    thumbnail_img = Gtk.Template.Child()

    has_thumbnail = GObject.Property(type=bool, default=False)
    game_name = GObject.Property(type=str, default='')

    def __init__(self, game: Game, system_config: SystemConfig) -> None:
        super().__init__()
        self.__game = game
        self.game_name = game.game_name

        thumbnail_path = game.thumbnail_path
        self.has_thumbnail = thumbnail_path is not None
        thumbnail_size = system_config.image_thumbnail_size
        self.thumbnail_box.set_size_request(thumbnail_size[0], thumbnail_size[1])
        if self.has_thumbnail:
            self.thumbnail_img.set_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(thumbnail_path, thumbnail_size[0], thumbnail_size[1]))

    @Gtk.Template.Callback()
    def on_play_btn_clicked(self, button: Gtk.Button) -> None:
        self.__game.run()
