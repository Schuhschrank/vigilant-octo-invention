from engine.Stage import Stage
from engine.Event import Event
from engine.Action import Action
from engine.TravelEvent import TravelEvent
from engine.current_stage import *
import tkinter

# STATE: dict = dict()

root = tkinter.Tk()
frame = tkinter.Frame(root, padx=256, pady=256)
frame.grid()

entry_text = tkinter.Label(frame)
entry_text.grid(column=0, row=0)
entry_text_var = tkinter.StringVar()
entry_text["textvariable"] = entry_text_var

stage_text = tkinter.Label(frame)
stage_text.grid(column=0, row=1)
stage_var = tkinter.StringVar()
stage_text["textvariable"] = stage_var

events = tkinter.Label(frame)
events.grid(column=0, row=2)
events_var = tkinter.StringVar()
events["textvariable"] = events_var

buttons: list[tkinter.Button] = []


def display_event(event: Event):
    if isinstance(event, TravelEvent):
        events_var.set("")
        entry_text_var.set(event.description)
    else:
        events_var.set(events_var.get() + event.description + "\n")


def render():
    global buttons

    stage_var.set(get_stage().description)

    for b in buttons:
        b.destroy()
    buttons = []
    actions = get_stage().get_performable_actions()
    for a, i in zip(actions, range(len(actions))):
        button = tkinter.Button(frame, text=a.description, command=a.attempt)
        button.grid(column=0, row=i+3)
        buttons.append(button)


def start(initial_stage: Stage):
    Event.on_triggered = display_event
    Action.on_performed = render
    set_stage(initial_stage)
    render()
    root.mainloop()
