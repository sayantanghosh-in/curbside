# Curbside — Implementation Plan

A food truck sim in the terminal, run by a local model.

This document describes **what to build and why**. It gives data shapes and function
contracts, not implementations — the code is yours to write.

---

## Where things stand

**Done**
- Module layout: `state.py`, `utils/constants.py`, `utils/helpers.py`, `main.py`
- Type model settled — `FoodComponent`, `Ingredient`, `MenuItem`, `GameState`
- Intro screen and copy constants
- `STARTING_INVENTORY` (12 components) and `MENU` (9 dishes), validated: every
  ingredient reference resolves and every margin is positive

**Next — Phase 1, still stdlib only**
1. `can_make(item, inventory) -> bool` — one line now that inventory is a dict
2. `serve(item, state) -> bool`
3. `generate_order() -> dict`
4. `phrase_order(order) -> str` — hardcoded f-string, the LLM replaces this later
5. the `while True` loop

**Loose ends**
- `new_game` is annotated `-> UUID`; nodes must return state. Fix when wiring the graph.
- `GameState` has no `reputation`, `day`, or `served` yet. Reputation is what makes the
  customer quirks bite.

---

## The one rule

> **Python decides. The model phrases and classifies.**

The model never owns game state. It never invents an order, a price, or a stock level.
It does exactly two jobs:

1. Turn a structured order into a natural sentence a customer would say
2. Turn the player's free-text reply into one of four known intents

Everything else — stock, money, reputation, whether an order can be fulfilled — is
ordinary Python. This is what makes the game unbreakable regardless of what the model
says, and it's the property to protect as the project grows.

---

## Data shapes

These are settled. Defined in `state.py`, populated in `utils/constants.py`.

```python
class FoodComponent(TypedDict):     # a thing in the pantry
    name: str
    remaining_units: int
    cost_price_per_unit: int
    min_purchasable_quantity: int   # restocking buys in packs
    is_spicy: bool
    is_allergen: bool

class Ingredient(TypedDict):        # a line in a recipe
    food_component_name: str        # reference into inventory, NOT a copy
    units_needed: int

class MenuItem(TypedDict):
    name: str
    price: int
    ingredients: Sequence[Ingredient]

class GameState(TypedDict):
    id: UUID                            # save slot; becomes thread_id later
    money: int
    inventory: dict[str, FoodComponent] # single source of truth for stock
    menu: Sequence[MenuItem]
```

Two decisions worth keeping:

**`Ingredient` references by name rather than embedding a `FoodComponent`.** Stock lives
in exactly one place. Embedding would leave every dish carrying a stale copy of
`remaining_units` the moment anything is served.

**`inventory` is a dict, not a list.** Turns `can_make` from a nested search into a
comprehension.

Keep `GameState` flat and JSON-serialisable — the checkpointer in Phase 4 has to
round-trip it.

### Balance built into the data

- `tortilla` appears in 7 of 9 dishes — running out takes most of the menu down at once
- `cheese` starts at 6 units and every cheese dish needs 2 — three servings before the
  first restock decision
- 4 allergens (cheese, sour cream, tofu, peanut sauce), 2 spicy (salsa, jalapeno), so
  the `is_allergen` / `is_spicy` flags have real dishes behind them
- Margins run $3–$7; loaded nachos is the thinnest and most fragile

### Order (generated in Python, never by the model)

```python
order = {
    "items": list[tuple[str, int]],   # [("chicken burrito", 2)]
    "quirk": {"id": str, "note": str | None},
}
```

The **quirk** is the interesting part. `id` is a machine-checkable tag; `note` is the
hint the model uses to phrase it. Because `id` is structured, Python can verify whether
the player handled it — that's what makes this a game with rules rather than a chatbot.

Suggested quirks: `none`, `no_cheese`, `hurry`, `indecisive`, `group`.

---

## Phase 1 — the loop, no AI

**Goal:** a playable game with zero dependencies. *(In progress — data and types done.)*

Build:

```python
def can_make(item: MenuItem, inventory: dict[str, FoodComponent]) -> bool
def serve(item: MenuItem, qty: int, state: GameState) -> bool   # returns success
def generate_order() -> dict                                    # random item + qty + quirk
def phrase_order(order: dict) -> str                            # hardcoded f-string for now
def show_status(state: GameState) -> None
```

Main loop: generate an order → print the phrased sentence → read input → resolve →
print result → repeat. Commands: an item name, `stock`, `quit`.

**`phrase_order` is deliberately a stub.** In Phase 2 you replace its body and nothing
else changes. That's the seam.

**Done when:** you can serve a customer, watch stock go down and money go up, and quit.

---

## Phase 2 — the model plays the customer

**Goal:** replace two function bodies. No structural change.

### 2a. Phrasing

```python
def phrase_order(order: dict) -> str
```

Same signature as Phase 1. Now calls the model with the order and the quirk note, asking
for one or two short casual sentences.

⚠️ **Use `temperature=0.7` here.** You want varied phrasing — the same order twice should
not produce the same sentence.

### 2b. Parsing the player's reply

```python
class Reply(BaseModel):
    intent: Literal["accept", "decline", "substitute", "question"]
    substitute_item: str | None = None

def parse_reply(text: str, order: dict) -> Reply
```

Use `with_structured_output(Reply)`. Give the model the order, the menu, and the reply.

⚠️ **Use `temperature=0` here.** The same reply must classify the same way every time.
Two model instances, two settings, two jobs.

### 2c. Resolving intent

Pure Python. `accept` → serve the order. `substitute` → serve `substitute_item` instead,
if it's on the menu and in stock. `decline` → nothing sold, reputation cost. `question` →
answer from state, don't advance the turn.

### Quirk enforcement

```python
def check_quirk(order: dict, served_item: str, state: dict) -> None
```

Example: quirk `no_cheese` and the served item's `needs` contains cheese → reputation
drops. Deterministic, checkable, no model involved.

**Done when:** customers sound different each time, `"sure"` / `"coming up"` / `"yep"` all
resolve to `accept`, and serving cheese to the allergic customer costs you reputation.

### Config for this phase

```python
ChatOllama(model="qwen2.5:7b", temperature=0.7, num_ctx=8192)   # phrasing
ChatOllama(model="qwen2.5:7b", temperature=0.0, num_ctx=8192)   # parsing
```

`num_ctx=8192` matters — the 4096 default causes stalls on longer prompts.

---

## Phase 3 — into LangGraph

**Goal:** same game, wired as a graph. Logic unchanged.

Nodes, one per function you already have:

```
spawn_customer  → phrase_order  → [wait for input] → parse_reply → resolve → respond
```

State becomes a `TypedDict`. Nodes return **only the keys they changed**, never the whole
state — that habit matters once reducers exist.

A conditional edge after `parse_reply` routes on `intent`.

**Done when:** `app.invoke()` produces the same behaviour as Phase 2.

---

## Phase 4 — save and resume

```python
from langgraph.checkpoint.sqlite import SqliteSaver
```

One file, no Docker. `thread_id` identifies the save slot; use `"default"`.

**Done when:** you quit mid-shift, restart the process, and money, stock, and reputation
are exactly as you left them.

---

## Phase 5 — tools and the ReAct loop

Three tools, no more:

```python
@tool
def check_stock(ingredient: str) -> str
@tool
def price_lookup(item: str) -> str
@tool
def restock(ingredient: str, units: int) -> str
```

Bind them to the model, add a `ToolNode`, and close the loop back to the agent node. The
docstring is the only thing the model sees when choosing — write it for a colleague, not
as a code comment.

**Done when:** the model checks stock, finds it short, and offers a substitute unprompted.

---

## Phase 6 — human in the loop

```python
from langgraph.types import interrupt
```

Put it in front of anything irreversible or expensive: restocking (costs money), refunds,
closing for the day.

**Done when:** you can Ctrl+C at the restock prompt, restart, and land back at the same
question.

---

## Phase 7 — recipes via RAG

`data/recipes/` — one short markdown file per dish: ingredients, prep time, substitutions.

```python
def find_recipes(query: str, k: int = 3) -> list[str]
```

Embed the files once at startup with `nomic-embed-text`, embed the query, rank by cosine
similarity with numpy. **No vector database** — ten recipes in a list is the right tool at
this size, and knowing that is worth more than installing pgvector to prove you can.

The query varies genuinely each turn ("what can I make with tortillas and no cheese"),
which is what makes retrieval worth having here.

**Done when:** `"what can I make right now"` returns dishes you actually have stock for.

---

## Phase 8 — skills and guardrails

```
skills/
  upsell/SKILL.md            how to offer a bigger order without being pushy
  complaint/SKILL.md         how to handle an unhappy customer
  guardrails/scope.md        stay in character; refuse off-topic requests
```

Load the frontmatter (`name`, `description`) of every skill into the system prompt at
startup. Load the body only when the model names one. That's progressive disclosure — the
catalogue is cheap, the body loads on demand.

**Done when:** asking the truck to write Python gets a polite redirect instead of Python.

---

## Gotchas already paid for

- **`num_ctx=8192`.** Ollama defaults to 4096 regardless of what the model supports. Too
  small causes stalls that look like hangs.
- **Two temperatures.** 0.7 for generating text a human reads, 0.0 for classification.
- **Never `.format()` an f-string.** It breaks the moment content contains `{`.
- **Return only changed keys** from graph nodes.
- **When the model repeatedly gets enumeration wrong, move the enumeration into Python.**
  Give it a fixed list and ask it only to classify against that list.
- **`Field(description=...)` is prompt engineering**, not documentation — it's sent to the
  model as part of the schema.

---

## Stop points

Any of these is a complete, demoable thing:

- **After Phase 2** — a working game with an LLM customer
- **After Phase 4** — persistent state across sessions
- **After Phase 6** — the full agent stack minus retrieval

Later phases add coverage, not correctness. A finished Phase 4 beats a half-built Phase 7.
