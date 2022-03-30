import engine as e

# Fantasy little game

has_picked_up_stick = e.new_variable(False)

game_over = e.Stage(
    name="Game over",
    description="You died. Try again by restarting the game."
)
game_over.set_image("default_image.png")

forest = e.Stage(
    name="Forest",
    description="You are in an unknown forest. Dead leaves are everywhere. "
                "You see a stick with an interesting shape."
)
forest.set_image("default_image.png")

trail = e.Stage(
    name="Trail",
    description="There are flowers where the trail follows, and a sort of sweet music coming from behind."
)
trail.set_image("default_image.png")

campfire = e.Stage(
    name="Campfire",
    description="You discovered three things: a campfire is nearby, its ashes are still warm, "
                "and the music is coming from the stick.\n"
                "Soon it will be dark."
)
campfire.set_image("default_image.png")

walk_around = e.TravelAction(
    new_stage=trail,
    description="Walk around and look for a trail.",
    success_text="You have encountered a trail."
)

pick_leaf = e.TravelAction(
    new_stage=game_over,
    description="Kneel and examine one leaf.",
    success_text="There is a trap beneath the leaf. It was nice meeting you."
)

pick_stick = e.Action(
    description="Pick up the stick.",
    success_text="You collected the stick.",
    consequences=[(has_picked_up_stick, True)],
    prerequisites=lambda: not has_picked_up_stick.value
)

follow_music = e.TravelAction(
    new_stage=campfire,
    description="Follow the music.",
    success_text="You can now hear the music and start to follow it.",
    failure_text="Suddenly the music fades away. Perhaps you need help to hear.",
    condition=lambda: has_picked_up_stick.value
)

go_back_to_forest = e.TravelAction(
    new_stage=forest,
    description="Go back to the forest.",
    success_text="You went back."
)

stay_at_campfire = e.TravelAction(
    new_stage=game_over,
    description="Stay at the campfire for the night.",
    success_text="The campfire owners returned. "
                 "How unfortunate, they crossed your heart with an arrow before you could say something."
)

listen_to_stick = e.Action(
    description="Continue to follow the stick's directions.",
    success_text="You keep following the music. "
                 "Who knows what wonders are out there for your discovery."
)

go_back_to_trail = e.TravelAction(
    new_stage=trail,
    description="Go back to the trail.",
    success_text="You went back to the trail."
)

restart_game = e.TravelAction(
    new_stage=forest,
    description="Restart the game.",
    success_text="A new game has started.",
    consequences=[(has_picked_up_stick, False)]
)


forest.add_actions([pick_leaf, pick_stick, walk_around])
trail.add_actions([follow_music, go_back_to_forest])
campfire.add_actions([stay_at_campfire, listen_to_stick])
game_over.add_actions([restart_game])
e.start(forest)
