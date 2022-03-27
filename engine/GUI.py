from engine.framework import *

import tkinter as tk
from tkinter import ttk

_root = tk.Tk()
"""Application window"""

_root.title("Game")
# root.geometry("1280x720+50+50")
# root.resizable(False, False)
# root.attributes('-alpha', 0.5)

frame = ttk.Frame(_root, borderwidth=64)
frame.pack()


def _add_text_label() -> tk.StringVar:
    label = ttk.Label(frame, relief=tk.FLAT, padding=8)
    label.pack()
    string_var = tk.StringVar()
    label["textvariable"] = string_var
    return string_var


def _add_image_label() -> tk.Label:
    label = ttk.Label(frame)
    label.pack()
    return label


stage_title = ttk.Label(frame, font=("Arial", 16), relief=tk.RAISED, anchor=tk.CENTER, padding=(16, 8))
stage_title.pack(fill='x', )
entry_text = _add_text_label()
stage_image = _add_image_label()
stage_var = _add_text_label()
events_var = _add_text_label()
buttons: list[tk.Button] = []

buttons_frame = ttk.Frame(frame)
buttons_frame.pack()


def _process_action(action: Action, was_successful: bool):
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

    stage_title["text"] = stage().name

    stage_var.set(stage().description)
    stage_image.configure(image=stage().image)

    for b in buttons:
        b.destroy()
    buttons = []
    actions = stage().actions
    for a, i in zip(actions, range(len(actions))):
        if a.can_attempt():
            button = ttk.Button(buttons_frame, text=a.description, command=a.attempt, padding=(8, 4))
            button.pack(fill="x")
            buttons.append(button)


def start():
    Action.on_performed = _process_action
    render()
    _root.mainloop()
