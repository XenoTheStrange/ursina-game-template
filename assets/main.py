#!/usr/bin/python3
"""This will initialize the game, logging and start first scene"""

import argparse
import ursina as u
from scripts.logger import log
from scripts import manager
import sys

sys.dont_write_bytecode = True


def parse_arguments():
    parser = argparse.ArgumentParser(description="A port of Sonny 2 by Krin (Via ArmorGames)")
    parser.add_argument("--debug", action='store_true', help="Run in debug mode")
    return parser.parse_args()

#Configure the app window
#Icon does not display on linux? Active-x Default icon displays.
def configure_app():
    args = parse_arguments()
    if args.debug:
        manager.devmode = True
    u.window.setFixedSize(True)
    app = u.Ursina(title="Sonny 2", icon="./textures/ursina.ico", fullscreen=True, borderless=False, forced_aspect_ratio=16/9)
    return app

if __name__ == '__main__':
    log.info("Launching game...")
    app = configure_app()
    manager.initialize()
    app.run()
