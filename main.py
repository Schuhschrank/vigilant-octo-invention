import engine as e
from engine.state import get_state

# Demo game

get_state().update({
    "must_poop": True,
    "pants_down": False,
    "hunger_level": 1
})

toilet = e.Stage("You are sitting on a toilet.")
hallway = e.Stage("You are in the hallway.")

poop = e.Action("Take a dump.", "You took a massive shit. Oh my...",
                "You cannot poop! You still have your pants up!", auto_disable=True)
poop.conditions = {"pants_down": True, "must_poop": True}
poop.consequences = {"pooped": True, "must_poop": False}

pants_down = e.Action("Lower your pants.", "Your lowered your pants and can poop now.", auto_disable=True)
pants_down.consequences = {"pants_down": True}

enter_hallway = e.TravelAction(hallway, "Leave toilet.", "You entered the hallway.")
enter_hallway.prerequisites = {"pooped": True}

enter_toilet = e.TravelAction(toilet, "Enter toilet.", "You entered the toilet.")

toilet += [poop, pants_down, enter_hallway]
hallway += [enter_toilet]

e.start(toilet)
