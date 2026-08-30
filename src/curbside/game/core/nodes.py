# local imports
from curbside.state import GameState
from curbside.utils.constants import CLOSE_SHOP_MESSAGE, SUPPORTED_COMMANDS, NO_SAVED_GAME, STAR_FILLED

#  node to handle the open shop function
def open_shop(state: GameState) -> GameState:
    """
    This node is responsible to handle all the logic related to opening the shop.
    - It displays the current game state
    - A subgraph originates from this node that handles the full shop loop
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
        customers_ratio = f"\n{state['total_customers_served']}/{state['total_customers_arrived']} customers served"
        reputation = f"Store reputation: {STAR_FILLED} {state['reputation']:.2f}"
        print(f"{customers_ratio} --- {reputation}")
    print(CLOSE_SHOP_MESSAGE)
    return state;

# node to check the current inventory
def check_inventory(state: GameState) -> GameState:
    """
    This node prints the current inventory at a menu item level
    """
    if state['id'] and isinstance(state['inventory'], dict):
        for key, value in state['inventory'].items():
            print(f"{key} -> {value['remaining_units']}")
    return state;

# node to order menu items for the inventory
def order_inventory(state: GameState) -> GameState:
    """
    - This node is responsible for the restocking of the inventory.
    - A subgraph originates from this node that handles the full ordering workflow.
    - deduct money min_order_quantity * cost_price_per_unit
    - increase inventory item by min_order_quantity
    """
    print("""
    TODO - build the ordering flow""")
    return state;
