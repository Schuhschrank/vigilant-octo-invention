from engine.Stage import Stage
from engine.Action import Action
from engine.TravelAction import TravelAction
from engine.staging import set_stage, get_stage
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


def process_action(action: Action, was_successful: bool):
    if was_successful:
        if isinstance(action, TravelAction):
            entry_text_var.set(action.success_text)
            events_var.set("")
        else:
            events_var.set(events_var.get() + action.success_text + "\n")
    else:
        events_var.set(events_var.get() + action.failure_text + "\n")
    render()


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
    Action.on_performed = process_action
    set_stage(initial_stage)
    render()
    root.mainloop()
