from curbside.state import GameState, FoodComponent, MenuItem

CURBSIDE_ASCII_LOGO = """
██████ ██  ██ ██████  ██████  ██████ ██ ██████  ██████
██     ██  ██ ██  ██  ██  ██  ██     ██ ██  ██  ██
██     ██  ██ ██████  ██████  ██████ ██ ██  ██  ██████
██     ██  ██ ██  ██  ██  ██      ██ ██ ██  ██  ██
██████ ██████ ██  ██  ██████  ██████ ██ ██████  ██████
"""

CURBSIDE_GAME_DESCRIPTION = """
version: 0.1.0
author: Sayantan Ghosh (https://sayantanghosh.in)
raise issues: https://github.com/sayantanghosh-in/curbside/issues

Please show some love ❤️ by starring ⭐️ this project on Github.

a food truck sim, run by a model on your machine.
open the window. take the orders. don't run out of cheese.
lunch rush, locally hosted"""

SAVED_STATE_PRESENT = """
It seems you have a saved game.
Type: `/` [press Enter] to start a new game or `/commands` [press ENTER] for the list of supported commands in game."""

SAVED_STATE_ABSENT_INTRO = """
Tip: Have a natural conversation with your customers.
Type: `/` [press Enter] to start a new game or `/commands` [press ENTER] for the list of supported commands in game."""

NO_SAVED_GAME = """
Could not find a saved game... Taking you back to the main menu."""

INVALID_USER_COMMAND = """
You entered an invalid command."""

STAR_FILLED = "⭐️"
STAR_OUTLINE = "✩"

MAX_REPUTATION = 5
STARTING_MONEY = 340

SUPPORTED_COMMANDS = """
Here's a list of supported commands:

/commands - shows the list of all supported commands in the game
/open - Opens the shop and starts the game"""

CLOSE_SHOP_MESSAGE = """
Bye, see you again!"""

BASE_GAME_STATE: GameState = {
    "id": None,
    "inventory": None,
    "menu": [],
    "money": 0,
    "reputation": 0,
    "total_customers_arrived": 0,
    "total_customers_served": 0,
    "total_penalties": 0,
    "user_inputs": []
}


# ---------------------------------------------------------------------------
# Pantry
#
# cost_price_per_unit      what you pay to restock one unit
# min_purchasable_quantity restocking buys at least this many (you buy in packs)
# is_allergen              flags the "no allergens" customer quirk
# is_spicy                 flags the "nothing spicy" customer quirk
# ---------------------------------------------------------------------------

STARTING_INVENTORY: dict[str, FoodComponent] = {
    "tortilla": {
        "name": "tortilla",
        "remaining_units": 18,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 12,
        "is_spicy": False,
        "is_allergen": False,
    },
    "rice": {
        "name": "rice",
        "remaining_units": 10,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 10,
        "is_spicy": False,
        "is_allergen": False,
    },
    "beans": {
        "name": "beans",
        "remaining_units": 12,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 10,
        "is_spicy": False,
        "is_allergen": False,
    },
    "veggies": {
        "name": "veggies",
        "remaining_units": 12,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 10,
        "is_spicy": False,
        "is_allergen": False,
    },
    "chicken": {
        "name": "chicken",
        "remaining_units": 9,
        "cost_price_per_unit": 3,
        "min_purchasable_quantity": 6,
        "is_spicy": False,
        "is_allergen": False,
    },
    "cheese": {
        "name": "cheese",
        "remaining_units": 6,
        "cost_price_per_unit": 2,
        "min_purchasable_quantity": 8,
        "is_spicy": False,
        "is_allergen": True,
    },
    "sour cream": {
        "name": "sour cream",
        "remaining_units": 7,
        "cost_price_per_unit": 2,
        "min_purchasable_quantity": 6,
        "is_spicy": False,
        "is_allergen": True,
    },
    "tofu": {
        "name": "tofu",
        "remaining_units": 8,
        "cost_price_per_unit": 2,
        "min_purchasable_quantity": 6,
        "is_spicy": False,
        "is_allergen": True,
    },
    "peanut sauce": {
        "name": "peanut sauce",
        "remaining_units": 4,
        "cost_price_per_unit": 3,
        "min_purchasable_quantity": 4,
        "is_spicy": False,
        "is_allergen": True,
    },
    "guacamole": {
        "name": "guacamole",
        "remaining_units": 6,
        "cost_price_per_unit": 3,
        "min_purchasable_quantity": 4,
        "is_spicy": False,
        "is_allergen": False,
    },
    "salsa": {
        "name": "salsa",
        "remaining_units": 8,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 6,
        "is_spicy": True,
        "is_allergen": False,
    },
    "jalapeno": {
        "name": "jalapeno",
        "remaining_units": 5,
        "cost_price_per_unit": 1,
        "min_purchasable_quantity": 6,
        "is_spicy": True,
        "is_allergen": False,
    },
}


# ---------------------------------------------------------------------------
# Menu
#
# Ingredients deliberately overlap: tortilla appears in 7 of 9 dishes, so
# running out of it takes most of the menu down at once. Cheese starts at 6
# units and every cheese dish needs 2 — three servings before your first
# real decision.
# ---------------------------------------------------------------------------

MENU: list[MenuItem] = [
    {
        "name": "veggie wrap",
        "price": 8,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "veggies", "units_needed": 1},
        ],
    },
    {
        "name": "bean bowl",
        "price": 7,
        "ingredients": [
            {"food_component_name": "beans", "units_needed": 1},
            {"food_component_name": "rice", "units_needed": 1},
            {"food_component_name": "veggies", "units_needed": 1},
        ],
    },
    {
        "name": "quesadilla",
        "price": 9,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "cheese", "units_needed": 2},
        ],
    },
    {
        "name": "loaded nachos",
        "price": 11,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 2},
            {"food_component_name": "cheese", "units_needed": 2},
            {"food_component_name": "beans", "units_needed": 1},
            {"food_component_name": "salsa", "units_needed": 1},
        ],
    },
    {
        "name": "chicken burrito",
        "price": 12,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "chicken", "units_needed": 1},
            {"food_component_name": "rice", "units_needed": 1},
            {"food_component_name": "beans", "units_needed": 1},
        ],
    },
    {
        "name": "chicken quesadilla",
        "price": 13,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "chicken", "units_needed": 1},
            {"food_component_name": "cheese", "units_needed": 2},
        ],
    },
    {
        "name": "guac burrito",
        "price": 13,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "beans", "units_needed": 1},
            {"food_component_name": "rice", "units_needed": 1},
            {"food_component_name": "guacamole", "units_needed": 1},
        ],
    },
    {
        "name": "spicy tofu bowl",
        "price": 10,
        "ingredients": [
            {"food_component_name": "tofu", "units_needed": 1},
            {"food_component_name": "rice", "units_needed": 1},
            {"food_component_name": "jalapeno", "units_needed": 1},
            {"food_component_name": "veggies", "units_needed": 1},
        ],
    },
    {
        "name": "peanut chicken wrap",
        "price": 13,
        "ingredients": [
            {"food_component_name": "tortilla", "units_needed": 1},
            {"food_component_name": "chicken", "units_needed": 1},
            {"food_component_name": "peanut sauce", "units_needed": 1},
            {"food_component_name": "veggies", "units_needed": 1},
        ],
    },
]