import os
import sys
from retro_game_launcher.backend import utility
from retro_game_launcher.frontend.application import RetroGameLauncherApp

def main(version):
    # Ensure that the config directory exists
    config_dir = utility.user_config_directory()
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Run the application
    app = RetroGameLauncherApp()
    return app.run(sys.argv)

