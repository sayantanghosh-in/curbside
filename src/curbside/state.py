from typing import Sequence, TypedDict, Optional
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
    id: Optional[UUID] # uuid - later on, can be used to differentiate between multiple saved states
    money: Optional[int]
    inventory: Optional[dict[str, FoodComponent]] # {name: component}
    menu: Optional[Sequence[MenuItem]]
    reputation: Optional[float] # the star rating
    total_customers_arrived: Optional[int]
    total_customers_served: Optional[int]
    total_penalties: Optional[int] # total amount of money deducted for any reason
    user_inputs: Optional[Sequence[str]]