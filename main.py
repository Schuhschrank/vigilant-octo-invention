import engine as e

# Demo game

save_progress = e.Action("Save your progress.", auto_disable=True, effects=[])
progress_saved = e.Event("Progress saved.")
save_progress.effects.append(progress_saved)

turn_off_computer = e.Action("Turn off the computer", auto_disable=True,
                             effects=[e.Event("The computer is turned off.")])
failed_shutdown = e.Event("The computer won't turn off.")
turn_off_computer.fail_event = failed_shutdown
turn_off_computer.conditions.append(progress_saved)

at_the_computer = e.Stage("You are sitting at the computer.", [turn_off_computer, save_progress])

e.start(at_the_computer)
