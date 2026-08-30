import random
from uuid import uuid4
from typing import Optional
# local imports
from curbside.state import FoodComponent, FoodOrder, MenuItem, GameState

def can_make(food: MenuItem | None, inventory: Optional[dict[str, FoodComponent]]) -> bool:
    """This function calculates if there are enough ingredients to cook the food. Returns True or False"""
    if not isinstance(inventory, dict) or not food:
        return False
    can = True
    ingredients = food['ingredients']
    for ingredient in ingredients:
        if ingredient['units_needed'] > inventory[ingredient['food_component_name']]['remaining_units']:
            can = False;
            break;
    return can

def serve(state: GameState) -> GameState:
    """
    - This function serves the food to the customer.
    - We deduct the `units_needed` quantity of the FoodComponent in the inventory.
    - Update the is_served value of the corresponding food order
    - increment the total customers served
    """
    if not isinstance(state['inventory'], dict) or not isinstance(state['menu'], list) or not isinstance(state['food_orders'], list):
        return state
    menu_item: Optional[MenuItem] = None
    food_order = state['food_orders'][-1] # the last order
    for food_item in food_order['food_items']:
        for item in state['menu']:
            if item['name'] == food_item:
                menu_item = item
            else:
                menu_item = None
            if menu_item and isinstance(state['money'], int) and can_make(menu_item, state['inventory']):
                # increase the money for this foot item
                state['money'] += menu_item['price']
                state['food_orders'][-1]['number_of_served_items'] += 1
                # deduct the ingredients for this food item
                for ingredient in menu_item['ingredients']:
                    state['inventory'][ingredient['food_component_name']]['remaining_units'] -= ingredient['units_needed']
    if isinstance(state['total_customers_served'], int):
        state['total_customers_served'] += 1
    return state

def generate_order(state: GameState) -> FoodOrder | None:
    """
    This function will be used by the LLM to create an order.
    The logic will take into consideration, the menu catalogue.
    It may order any item in the menu.
    An order can consist of 1 or more (max 3) types of food items.
    The total customers arrived to be incremented
    """
    if not state['menu']:
        return None
    random_food_items_count = random.randint(1,3)
    food_items = []
    for _ in range(random_food_items_count):
        # choose a random menu item
        food_items.append(random.choice(state['menu'])['name'])
    order = FoodOrder(id=uuid4(), food_items=food_items, number_of_served_items=0, total_number_of_items=len(food_items))
    if isinstance(state['food_orders'], list) and isinstance(state['total_customers_arrived'], int):
        state['food_orders'].append(order)
        state['total_customers_arrived'] += 1
    else:
        state['food_orders'] = [order]
    return order