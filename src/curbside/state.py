from typing import Sequence, TypedDict
from uuid import UUID

class FoodComponent(TypedDict):
    name: str
    remaining_units: int
    cost_price_per_unit: int
    min_purchasable_quantity: int
    is_spicy: bool
    is_allergen: bool

class Ingredient(TypedDict):
    food_component_name: str
    units_needed: int

class MenuItem(TypedDict):
    name: str
    price: int
    ingredients: Sequence[Ingredient]

class GameState(TypedDict):
    id: UUID # uuid - later on, can be used to differentiate between multiple saved states
    money: int
    inventory: dict[str, FoodComponent] # {name: component}
    menu: Sequence[MenuItem]