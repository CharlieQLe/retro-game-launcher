import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, GdkPixbuf, Gio, Gtk, GObject
from retro_game_launcher.backend import utility
from retro_game_launcher.backend.config import SystemConfig
from retro_game_launcher.frontend.game import Game
from retro_game_launcher.frontend.widgets.game_item import GameItem

@Gtk.Template(resource_path='/com/charlieqle/RetroGameLauncher/ui/game_view.ui')
class GameView(Gtk.Box):
    """
    The game view.

    Attributes:
        factory (Gtk.SignalListItemFactory): The factory to generate the list items.
        games (Gio.ListStore): The list store that stores the games.
        has_games (bool): Determines if there are games or not.
        none_title (str): The title of the no games status page.
        none_description (str): The description of the no games status page.
        none_icon_name (str): The icon name of the no games status page.
        system_config (SystemConfig): The configuration of the system that this view belongs to.
    """

    __gtype_name__ = 'GameView'

    none_found = Gtk.Template.Child()
    found = Gtk.Template.Child()
    model_view = Gtk.Template.Child()

    factory: Gtk.SignalListItemFactory = GObject.Property(type=Gtk.SignalListItemFactory, default=None)
    games: Gio.ListStore = GObject.Property(type=Gio.ListStore, default=None)
    has_games: bool = GObject.Property(type=bool, default=False)
    none_title: str = GObject.Property(type=str, default='No games found')
    none_description: str = GObject.Property(type=str, default='Add games!')
    none_icon_name: str = GObject.Property(type=str, default='applications-games-symbolic')

    def __init__(self, **kwargs) -> None:
        """
        Initialize this game view.
        """
        super().__init__(**kwargs)

        self.factory = Gtk.SignalListItemFactory()
        self.factory.connect('bind', self.on_factory_bind)
        self.games = Gio.ListStore.new(Game)
        self.__system_config: SystemConfig = None

    def set_system_config(self, system_config: SystemConfig) -> None:
        """
        Set the system config.

        Parameters:
            system_config (SystemConfig): The configuration for the system this view is attached to.
        """
        self.__system_config = system_config

    def on_factory_bind(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem) -> None:
        """
        Handle all binds for the factory.

        Parameters:
            factory (Gtk.SignalListItemFactory): The factory that emitted this signal.
            item (Gtk.ListItem): The item that was bound.
        """
        item.set_activatable(False)
        item.set_child(GameItem(item.get_item(), self.__system_config))

    def clear_games(self) -> None:
        """
        Clear all games from this view.
        """
        self.games.remove_all()
        self.has_games = False

    def add_game(self, game: Game) -> None:
        """
        Add a game to this view.

        Parameters:
            game (Game): The game to add.
        """
        self.games.append(game)
        self.has_games = True

    def insert_game(self, position: int, game: Game) -> None:
        """
        Insert a game at the specified position within this view.

        Parameters:
            position (int): The position to insert at
            game (Game): The game to add
        """
        self.games.insert(position, game)

    def __len__(self) -> int:
        """
        Get the number of games in this view.

        Returns:
            int: The number of games
        """
        return len(self.games)

