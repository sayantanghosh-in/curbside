# local imports
from curbside.utils.constants import CURBSIDE_ASCII_LOGO, CURBSIDE_GAME_DESCRIPTION

def draw_intro_screen():
    print(CURBSIDE_ASCII_LOGO)
    print(CURBSIDE_GAME_DESCRIPTION)

def clear_terminal():
    print("\x1b[2J\x1b[H", end="")