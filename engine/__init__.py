from engine.Stage import Stage
from engine.Event import Event
from engine.Action import Action
import tkinter

STAGE: Stage = Stage("This is an empty stage.", [])

root = tkinter.Tk()
frame = tkinter.Frame(root, padx=256, pady=256)
frame.grid()

stage_text = tkinter.Label(frame)
stage_text.grid(column=0, row=0)
stage_var = tkinter.StringVar()
stage_text["textvariable"] = stage_var

events = tkinter.Label(frame)
events.grid(column=0, row=1)
events_var = tkinter.StringVar()
events["textvariable"] = events_var

buttons: list[tkinter.Button] = []


def display_event(event):
    events_var.set(events_var.get() + event.description + "\n")


def render():
    global buttons

    stage_var.set(STAGE.description)

    for b in buttons:
        b.destroy()
    buttons = []
    actions = STAGE.get_performable_actions()
    for a, i in zip(actions, range(len(actions))):
        button = tkinter.Button(frame, text=a.description, command=a.attempt)
        button.grid(column=0, row=i+2)
        buttons.append(button)


def start(stage: Stage):
    global STAGE

    # Event.on_triggered = display_event
    Action.on_performed = render
    STAGE = stage
    render()
    root.mainloop()
