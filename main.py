import engine as e

# Demo game

must_poop = e.add_var(True)
pants_down = e.add_var(False)
full = e.add_var(False)
pooped = e.add_var(False)
pooped_once = e.add_var(False)

toilet = e.Stage(
    name="Toilet",
    description="You are sitting on a toilet."
)
hallway = e.Stage(
    name="Hallway",
    description="You are in the hallway."
)
living_room = e.Stage(
    name="Living room",
    description="You are in the living room."
)
poop = e.Action(
    description="Take a dump! Do it quickly! My anus is dying!",
    success_text="You took a massive shit. Oh my...",
    failure_text="You cannot poop! You still have your pants up!",
    conditions={pants_down: True},
    consequences={pooped: True, must_poop: False, full: False, pooped_once: True},
    prerequisites={must_poop: True}
)
pants_down = e.Action(
    description="Lower your pants.",
    success_text="Your lowered your pants and can poop now.",
    consequences={pants_down: True},
    prerequisites={pants_down: False}
)
fart = e.Action(
    description="Release a fart.",
    success_text="Your fart stinks."
)
enter_hallway = e.TravelAction(
    new_stage=hallway,
    description="Leave toilet.",
    success_text="You entered the hallway.",
    prerequisites={pooped_once: True}
)
enter_toilet = e.TravelAction(
    new_stage=toilet,
    description="Enter toilet.",
    success_text="You entered the toilet."
)
enter_living_room = e.TravelAction(
    new_stage=living_room,
    description="Enter living room.",
    success_text="You entered the living room."
)
eat = e.Action(
    description="Eat a huge burger.",
    success_text="You feel very full now and you must poop again.",
    failure_text="You cannot eat.",
    conditions={pooped: True, full: False},
    consequences={must_poop: True, full: True}
)
toilet.add_actions([
    poop,
    pants_down,
    enter_hallway
])
hallway.add_actions([
    enter_toilet,
    eat,
    enter_living_room
])
living_room.add_actions([
    fart,
    enter_hallway
])

e.start(toilet)
