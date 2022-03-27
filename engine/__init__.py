from engine.Stage import Stage
from engine.Action import Action
from engine.TravelAction import TravelAction
from engine.staging import set_stage, get_stage
import tkinter

# STATE: dict = dict()

root = tkinter.Tk()
frame = tkinter.Frame(root, padx=256, pady=256)
frame.grid()


num_labels = 0


def add_label() -> tkinter.StringVar:
    global num_labels
    label = tkinter.Label(frame)
    label.grid(column=0, row=num_labels)
    num_labels += 1
    string_var = tkinter.StringVar()
    label["textvariable"] = string_var
    return string_var


title_text = add_label()
entry_text = add_label()
stage_var = add_label()
events_var = add_label()
buttons: list[tkinter.Button] = []


def process_action(action: Action, was_successful: bool):
    if was_successful:
        if isinstance(action, TravelAction):
            entry_text.set(action.success_text)
            events_var.set("")
        else:
            events_var.set(events_var.get() + action.success_text + "\n")
    else:
        events_var.set(events_var.get() + action.failure_text + "\n")
    render()


def render():
    global buttons

    title_text.set(get_stage().name)
    stage_var.set(get_stage().description)

    for b in buttons:
        b.destroy()
    buttons = []
    actions = get_stage().get_performable_actions()
    for a, i in zip(actions, range(len(actions))):
        button = tkinter.Button(frame, text=a.description, command=a.attempt)
        button.grid(column=0, row=i+num_labels)
        buttons.append(button)


def start(initial_stage: Stage):
    Action.on_performed = process_action
    set_stage(initial_stage)
    render()
    root.mainloop()
