import engine as e

# Demo game
import engine.Var as Vars

e.init()

e.settings.image_folder_path = "images/"

must_poop = Vars.new_variable(True)
are_pants_down = Vars.new_variable(False)
is_full = Vars.new_variable(False)
has_pooped = Vars.new_variable(False)
has_pooped_once = Vars.new_variable(False)

toilet = e.Stage(
    name="Toilet",
    description="You are sitting on the toilet."
)
toilet_paper = e.Prop("You see a role of toilet paper next to you.")
destroy_toilet_paper = e.Action(
    "Beam the toilet paper away with your mind.",
    "The toilet paper disappeared.",
    consequences=[
        (toilet_paper, "There is a stain beneath where the toilet paper was.")
    ],
    auto_disable=True
)
hallway = e.Stage(
    name="Hallway",
    description="You are in the hallway.",
    image_name="default_image.png"
)
hallway.set_image("default_image.png")
living_room = e.Stage(
    name="Living room",
    description="You are in the living room."
)
poop = e.Action(
    description="Take a dump.",
    success_text="You took a massive shit. Oh my...",
    failure_text="You cannot poop! You still have your pants up.",
    condition=lambda: are_pants_down.value,
    consequences=[
        (has_pooped, True), (must_poop, False), (is_full, False), (has_pooped_once, True)
    ],
    prerequisites=lambda: must_poop.value
)
pants_down = e.Action(
    description="Lower your pants.",
    success_text="Your lowered your pants and can poop now.",
    consequences=[(are_pants_down, True)],
    prerequisites=lambda: not are_pants_down.value
)
fart = e.Action(
    description="Release a fart.",
    success_text="Your fart stinks."
)
enter_hallway = e.TravelAction(new_stage=hallway, prerequisites=lambda: has_pooped_once.value)
enter_toilet = e.TravelAction(new_stage=toilet)
enter_living_room = e.TravelAction(new_stage=living_room)
eat = e.Action(
    description="Eat a huge burger.",
    success_text="You feel very full now and you must poop again.",
    failure_text="You cannot eat, you are full.",
    condition=lambda: has_pooped.value and not is_full.value,
    consequences=[(must_poop, True), (is_full, True)]
)
toilet.add_actions([
    poop,
    pants_down,
    destroy_toilet_paper,
    enter_hallway
])
toilet.props = [toilet_paper]
hallway.add_actions([
    eat,
    enter_living_room,
    enter_toilet,
])
living_room.add_actions([
    fart,
    enter_hallway
])

e.start(toilet, "My game")
