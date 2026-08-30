from typing import Literal
# local imports
from curbside.state import GameState
from curbside.utils.constants import SAVED_STATE_ABSENT_INTRO

# action to check if there is a saved checkpoint in the game
def check_game_saved_state(state: GameState) -> Literal["game_save_present", "game_save_absent"]:
    if state['id']:
        print()
        return "game_save_present"
    else:
        print(SAVED_STATE_ABSENT_INTRO)
        return "game_save_absent"