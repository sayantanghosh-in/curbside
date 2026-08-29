from uuid import uuid4, UUID
# local imports
from curbside.state import GameState
from curbside.utils.constants import SAVED_STATE_ABSENT
from curbside.utils.helpers import draw_intro_screen

# @TODO - action for the conditional edge to decide between 2 paths
def check_game_saved_state() -> bool:
    # @TODO - implement the real saved state
    is_saved_state_present = False
    if is_saved_state_present:
        print()
        return True
    else:
        print(SAVED_STATE_ABSENT)
        return False

# @TODO - node to load the saved game
def load_game(state: GameState) -> GameState:
    """This node loads the saved game state and resumes the game from the last saved checkpoint"""
    print("\nFound a saved game. Resuming...")
    return state

# @TODO - node to start a new game
def new_game(state: GameState) -> UUID:
    """This node starts a new game session, creates a new UUID for the game state."""
    print("\nNo saved game found. Starting new game...")
    game_uuid = uuid4()
    state["id"] = game_uuid
    return game_uuid

# @TODO - main game node that is the starting point
def game():
    # game started, show the intro screen
    draw_intro_screen()

    # check if there is a saved state of the game
    is_saved = check_game_saved_state()
    if is_saved:
        # load_game()
        pass
    else:
        # new_game()
        pass
