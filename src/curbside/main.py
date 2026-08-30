from typing import Literal
from uuid import uuid4, UUID
from langgraph.graph import StateGraph, START, END
import copy
# local imports
from curbside.game.core.graphs.open import open_shop_subgraph
from curbside.game.core.nodes import check_inventory, close_shop, show_all_commands, order_inventory
from curbside.state import GameState
from curbside.utils.constants import BASE_GAME_STATE, INVALID_USER_COMMAND, MENU, STARTING_INVENTORY, STARTING_MONEY
from curbside.utils.helpers import clear_terminal, draw_intro_screen

# @TODO - node to load the saved game
def load_game(state: GameState) -> GameState:
    """This node loads the saved game state and resumes the game from the last saved checkpoint"""
    print("\nFound a saved game. Resuming...")
    return state

# main game node
def game(state: GameState) -> GameState:
    """main game node that displays the intro message and handles the initial user command /. This node initializes the game."""
    # clear the screen
    clear_terminal()
    # game started, show the intro screen
    draw_intro_screen()
    input()
    # @TODO - for now, treat everything as a new game. load game coming soon
    state["id"] = uuid4()
    state["menu"] = MENU
    state["inventory"] = copy.deepcopy(STARTING_INVENTORY)
    state["money"] = STARTING_MONEY
    return state

# command handler node
def game_commands_handler(state: GameState) -> GameState:
    """command handler node that handles the user commands after the game is initialized"""
    user_input = input("> ")
    if user_input and isinstance(state["user_inputs"], list):
        state['user_inputs'].append(user_input)
    return state

# main game router
def main_game_router(state: GameState) -> Literal['check', 'open', 'close', 'commands', 'order']:
    """
    - This router function checks the entered user command.
    - If valid, it routes to a correct node.
    - If invalid, it prints a message and routes to the /commands path instead
    """
    if isinstance(state["user_inputs"], list) and len(state['user_inputs']) > 0:
        last_user_input = state['user_inputs'][-1]
        if last_user_input == '/open':
            return 'open'
        elif last_user_input == '/check':
            return 'check'
        elif last_user_input == '/close':
            return 'close'
        elif last_user_input == '/commands':
            return 'commands'
        elif last_user_input == '/order':
            return 'order'
    print(INVALID_USER_COMMAND)
    return 'commands'


# create the main graph
main_game_graph = StateGraph(GameState)

# add the nodes to the graph
main_game_graph.add_node("main_game", game)
main_game_graph.add_node("game_commands", game_commands_handler)
main_game_graph.add_node("check_inventory", check_inventory)
main_game_graph.add_node("close_shop", close_shop)
main_game_graph.add_node("open_shop", open_shop_subgraph)
main_game_graph.add_node("show_all_commands", show_all_commands)
main_game_graph.add_node("order_inventory", order_inventory)

# add the edges to the graph
main_game_graph.add_edge(START, "main_game")
main_game_graph.add_edge("main_game", "show_all_commands")
main_game_graph.add_conditional_edges(
    "game_commands",
    main_game_router,
    {
        # edge: node
        "close": "close_shop",
        "open": "open_shop",
        "commands": "show_all_commands",
        "check": "check_inventory",
        "order": "order_inventory"
    }
)
# @TODO - temporarily route the following nodes to the END node
main_game_graph.add_edge("check_inventory", "game_commands")
main_game_graph.add_edge("order_inventory", "game_commands")

# deterministic - route the following nodes to the END
main_game_graph.add_edge("close_shop", END)

# @TODO - temporarily route the open_shop node to the END node
main_game_graph.add_edge("open_shop", END)

# deterministic - route the following nodes to the game_commands
main_game_graph.add_edge("show_all_commands", "game_commands")

# compile the graph
app = main_game_graph.compile()

# invoke the compiled graph
def main():
    app.invoke(BASE_GAME_STATE)

if __name__ == '__main__':
    main()
