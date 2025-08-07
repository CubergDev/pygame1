# source/main.py

__author__ = 'from cuberg with love'

import os
import pygame as pg

from . import tool
from . import constants as c
from .state import mainmenu, screen, level

def main():
    # ─── Background music ─────────────────────────────────────────
    music_path = os.path.join("resources", "music", "background.ogg")
    try:
        pg.mixer.music.load(music_path)
        pg.mixer.music.set_volume(0.5)    # 0.0 to 1.0
        pg.mixer.music.play(loops=-1)     # loop indefinitely
    except pg.error as e:
        print(f"Could not play background music: {e}")
    # ─────────────────────────────────────────────────────────────────

    game = tool.Control()
    state_dict = {
        c.MAIN_MENU: mainmenu.Menu(),
        c.GAME_LOSE: screen.GameLoseScreen(),
        c.LEVEL:     level.Level()
    }
    game.setup_states(state_dict, c.MAIN_MENU)
    game.main()
