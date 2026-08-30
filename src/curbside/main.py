from typing import Literal
from uuid import uuid4, UUID
from langgraph.graph import StateGraph, START, END
# local imports
from curbside.game.core.nodes import close_shop, open_shop, show_all_commands
from curbside.state import GameState
from curbside.utils.constants import BASE_GAME_STATE, INVALID_USER_COMMAND
from curbside.utils.helpers import clear_terminal, draw_intro_screen

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

# main game node
def game(state: GameState) -> GameState:
    """main game node that displays the intro message and handles the initial user command inuts"""
    # clear the screen
    clear_terminal()
    # game started, show the intro screen
    draw_intro_screen()
    user_input = input("> ")
    if user_input and isinstance(state["user_inputs"], list):
        state['user_inputs'].append(user_input)
    return state

# main game router
def main_game_router(state: GameState) -> Literal['open', 'close', 'commands']:
    """
    - This router function checks the entered user command.
    - If valid, it routes to a correct node.
    - If invalid, it prints a message and routes to the /commands path instead
    """
    if isinstance(state["user_inputs"], list) and len(state['user_inputs']) > 0:
        last_user_input = state['user_inputs'][-1]
        if last_user_input == '/open':
            return 'open'
        elif last_user_input == '/close':
            return 'close'
        elif last_user_input == '/commands':
            return 'commands'
    print(INVALID_USER_COMMAND)
    return 'commands'


# create the main graph
main_game_graph = StateGraph(GameState)

# add the nodes to the graph
main_game_graph.add_node("main_game_node", game)
main_game_graph.add_node("close_shop", close_shop)
main_game_graph.add_node("open_shop", open_shop)
main_game_graph.add_node("show_all_commands", show_all_commands)

# add the edges to the graph
main_game_graph.add_edge(START, "main_game_node")
main_game_graph.add_conditional_edges(
    "main_game_node",
    main_game_router,
    {
        # edge: node
        "close": "close_shop",
        "open": "open_shop",
        "commands": "show_all_commands"
    }
)
main_game_graph.add_edge("close_shop", END)
# @TODO - temporarily route the open_shop node to the END node
main_game_graph.add_edge("open_shop", END)
# after showing the command, go back to the main game node
main_game_graph.add_edge("show_all_commands", "main_game_node")

# compile the graph
app = main_game_graph.compile()

# invoke the compiled graph
def main():
    app.invoke(BASE_GAME_STATE)

if __name__ == '__main__':
    main()
