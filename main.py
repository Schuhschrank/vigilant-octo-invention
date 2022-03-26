import engine as e

# Demo game

# Stage definitions
at_the_computer = e.Stage("You are sitting at the computer.")
shelf = e.Stage("You stand before a shelf. There are lots of things on it.")

# Actions and events
save_progress = e.Action("Save your progress.", auto_disable=True, consequences=[])
progress_saved = e.Event("Progress saved.")
save_progress.consequences.append(progress_saved)

turn_off_computer = e.Action("Turn off the computer", auto_disable=True,
                             consequences=[e.Event("The computer is turned off.")])
failed_shutdown = e.Event("The computer won't turn off.")
turn_off_computer.fail_event = failed_shutdown
turn_off_computer.conditions.append(progress_saved)

went_to_shelf = e.TravelEvent("You went to the shelf.", shelf)
goto_shelf = e.Action("Go to the shelf behind you.", consequences=[went_to_shelf])

took_book = e.Event("You took the book. It is in your bag now.")
take_book = e.Action("There is a book on astrophysics. Take it.", consequences=[took_book], auto_disable=True)

# Bindings of actions to stages
at_the_computer += [turn_off_computer, save_progress, goto_shelf]
shelf += [take_book]

e.start(at_the_computer)
