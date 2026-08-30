# local imports
from curbside.state import GameState
from curbside.utils.constants import CLOSE_SHOP_MESSAGE, SUPPORTED_COMMANDS, NO_SAVED_GAME, STAR_FILLED

#  node to handle the open shop function
def open_shop(state: GameState) -> GameState:
    """
    This node is responsible to handle all the logic related to opening the shop.
    - It displays the current game state
    """

    # check if the game save state is valid
    if state['id']:
        customers_ratio = f"{state['total_customers_served']}/{state['total_customers_arrived']}"
        reputation = f"{STAR_FILLED} {state['reputation']}"
        print(f"{customers_ratio} --- {reputation}")
    else:
        print(NO_SAVED_GAME)
    return state

# node to show all commands that are supported in the game
def show_all_commands(state: GameState) -> GameState:
    """This node prints all the in-game commands and simply returns the state"""
    print(SUPPORTED_COMMANDS)
    return state;

# node to close the shop
def close_shop(state: GameState) -> GameState:
    """
    This node is responsible to handle all the logic related to closing the shop.
    - It displays the current game state
    - It stores the current game state checkpoint
    """
    if state['id']:
        customers_ratio = f"{state['total_customers_served']}/{state['total_customers_arrived']}"
        reputation = f"{STAR_FILLED} {state['reputation']}"
        print(f"{customers_ratio} --- {reputation}")
    print(CLOSE_SHOP_MESSAGE)
    return state;
