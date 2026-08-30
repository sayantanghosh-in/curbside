from typing import Literal
from langgraph.graph import StateGraph, START, END
# local imports
from curbside.state import GameState, MenuItem
from curbside.game.core.nodes import close_shop, check_inventory
from curbside.game.core.logic import generate_order, serve
from curbside.utils.constants import APP_ERRORS

#  entry point to the open shop subgraph
def open_shop(state: GameState) -> GameState:
    """
    - This node is the starting of the open_shop subgraph.
    - This node creates a new order
    - Then proceeds to wait for user input
    """
    generate_order(state)
    new_order = None
    if state["food_orders"] is not None and isinstance(state["food_orders"], list):
        new_order = state["food_orders"][-1]
    if not new_order or not new_order['id'] or not isinstance(state['menu'], list):
        print(APP_ERRORS['ORDER_CREATION_FAILED'])
        return state

    sell_price = 0
    matching_menu_items: list[MenuItem] = []
    for item in state['menu']:
        if (item['name'] in new_order['food_items']):
            matching_menu_items.append(item)
            sell_price += item['price']
    formatted_item_list = ""
    for item in matching_menu_items:
        formatted_item_list += f"\n{item['name']}"
    print(f"""
    System: A new order is generated:
    Total price: {sell_price}
    Items:
    {formatted_item_list}""")
    return state

# node to accept the user input
def await_user_input(state: GameState) -> GameState:
    print(f"\nCommands supported: /check, /close and /serve. You can also type a custom message.")
    user_input = input(">")
    if user_input and isinstance(state["user_inputs"], list):
        state['user_inputs'].append(user_input)
    return state

# action handler that takes in user input and passes to the router
def handle_user_input(state: GameState) -> Literal['check', 'serve', 'close', 'custom']:
    """This function takes the user input from the last node and passes it to a conditional edge. The possible inputs are /check, /close, /serve and custom user input"""
    user_input = None
    if not isinstance(state['user_inputs'], list):
        print(APP_ERRORS['MALFORMED_STATE'])
    else:
        user_input = state['user_inputs'][-1]
    if state['user_inputs'] is not None:
        if user_input == '/check':
            return 'check'
        elif user_input == '/close':
            return 'close'
        elif user_input == '/serve':
            return 'serve'
        else:
            return "custom"
    return "close"

# node to serve food to the customer
def serve_food(state: GameState) -> GameState:
    """This node calls the serve function that mutates the game state and simply returns"""
    return serve(state)

# node to handle custom user input
def handle_custom_user_input(state: GameState) -> GameState:
    """
    - This node handles the custom user input with the help of LLM.
    - Structured output to be used so that it is one of clear, close or serve.
    - Any other derived format to be routed back to the user input node
    """
    return state

# graph
open_shop_graph = StateGraph(GameState)

# nodes
open_shop_graph.add_node("open_shop_main", open_shop)
open_shop_graph.add_node("open_shop_await_user_input", await_user_input)
open_shop_graph.add_node("open_shop_close", close_shop)
open_shop_graph.add_node("open_shop_check", check_inventory)
open_shop_graph.add_node("handle_custom_user_input", handle_custom_user_input)
open_shop_graph.add_node("serve_food", serve_food)

# edges
open_shop_graph.add_edge(START, "open_shop_main")
open_shop_graph.add_edge("open_shop_main", "open_shop_await_user_input")
open_shop_graph.add_conditional_edges(
    "open_shop_await_user_input",
    handle_user_input,
    {
        # "edge": "node"
        "close": "open_shop_close",
        "check": "open_shop_check",
        "serve": "serve_food",
        "custom": "handle_custom_user_input"
    }
)
open_shop_graph.add_edge("open_shop_close", END)
open_shop_graph.add_edge("open_shop_check", "open_shop_await_user_input")
open_shop_graph.add_edge("serve_food", "open_shop_main")
# @TODO - for now let this go to the END state
open_shop_graph.add_edge("handle_custom_user_input", END)

# compile — this is what main.py imports and adds as a node
open_shop_subgraph = open_shop_graph.compile()