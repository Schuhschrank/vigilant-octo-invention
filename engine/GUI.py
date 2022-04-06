import tkinter as tk
from tkinter import ttk

from engine.framework import *


_root = None
render_func = None


def init(window_title: str):
    global _root
    _root = tk.Tk()
    """Application's main window"""

    # _root.title("Game")
    # root.geometry("1280x720+50+50")
    # root.resizable(False, False)
    # root.attributes('-alpha', 0.5)

    frame = ttk.Frame(_root, borderwidth=64)
    frame.pack()

    stage_title = ttk.Label(frame, font=("Arial", 14), anchor=tk.CENTER)
    stage_title.pack()
    entrance_msg = ttk.Label(frame, text="The game has begun.")
    entrance_msg.pack()
    stage_label = ttk.Label(frame, compound=tk.TOP, relief=tk.GROOVE, padding=(8, 4),
                            wraplength=512)
    stage_label.pack()
    events_log = ttk.Label(frame, justify=tk.CENTER)
    events_log.pack()

    buttons: list[tk.Button] = []

    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack()

    def _process_action(action: Action, was_successful):
        if was_successful:
            if isinstance(action, TravelAction):
                entrance_msg["text"] = action.success_text
                events_log["text"] = ""
            else:
                if len(events_log['text']) > 0:
                    events_log["text"] = f"{events_log['text']}\n{action.success_text}"
                else:
                    events_log["text"] = action.success_text
        else:
            if len(events_log['text']) > 0:
                events_log["text"] = f"{events_log['text']}\n{action.failure_text}"
            else:
                events_log["text"] = action.failure_text
        render()

    class ActionProxy:

        def __init__(self, action: Action):
            self.action = action

        def attempt(self):
            was_successful = self.action.attempt()
            _process_action(self.action, was_successful)

    def render():
        nonlocal buttons

        stage_title["text"] = stage().name
        stage_label["text"] = stage().description

        if stage().image is not None:
            stage_label["image"] = stage().image
        else:
            stage_label.configure(image="")

        for b in buttons:
            b.destroy()
        buttons = []
        actions = stage().actions
        for a in actions:
            if a.can_attempt():
                proxy = ActionProxy(a)
                button = ttk.Button(buttons_frame, text=a.description, command=proxy.attempt,
                                    padding=(8, 4))
                button.pack(fill="x")
                buttons.append(button)
    global render_func
    render_func = render


def start_gui(window_title="GUI"):
    global _root
    _root.title = window_title
    render_func()
    _root.mainloop()
