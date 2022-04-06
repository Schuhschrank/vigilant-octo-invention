import tkinter as tk
from tkinter import ttk

import engine as e

from editor.Form import Form
from editor.ObjectManager import ObjectManager
from editor import serialization
from editor.utils import populate_obj


class Editor:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Editor")
        self.root.geometry("2300x900+0+0")

        self.obj_man = ObjectManager(self.root)

        stage_form = Form(self.root, self.obj_man, e.Stage)
        action_form = Form(self.root, self.obj_man, e.Action)
        prop_form = Form(self.root, self.obj_man, e.Prop)
        var_form = Form(self.root, self.obj_man, e.Var)
        statement_form = Form(self.root, self.obj_man, e.Statement)

        ttk.Button(self.root, text="Start game", command=self.start_game).pack(side="left")

        self.was_game_started = False

    def start(self):
        self.read_from_disk()
        self.root.mainloop()
        if not self.was_game_started:
            self.write_to_disk()

    def read_from_disk(self):
        try:
            with open("save") as file:
                env = {}
                current_line = 0
                lines = [line.rstrip() for line in file.readlines()]
                for t in [e.Var, e.Statement, e.Prop, e.Action, e.Stage]:
                    num_objs = int(lines[current_line])
                    current_line += 1
                    for _ in range(num_objs):
                        num_attr = int(lines[current_line])
                        begin = current_line + 1
                        end = begin + num_attr + 1
                        obj_def, identity = serialization.deserialize_obj(lines[begin:end], env)
                        obj = self.obj_man.new(t)
                        populate_obj(obj, obj_def)
                        env[identity] = obj
                        self.obj_man.update(obj)
                        current_line = end
                    print(f"Loaded objects of type {t}.")
        except FileNotFoundError:
            pass

    def write_to_disk(self):
        with open("save", "w") as file:
            for obj_type in [e.Var, e.Statement, e.Prop, e.Action, e.Stage]:
                objs: list[object] = self.obj_man.get(obj_type)
                file.write(f"{len(objs)}\n")
                for obj in objs:
                    file.write(serialization.serialize(obj))

    def start_game(self):
        self.was_game_started = True
        self.write_to_disk()
        self.root.destroy()
        e.init()
        stages = self.obj_man.get(e.Stage)
        initial_stage: e.Stage | None = None
        for s in stages:
            if s.name == "start":
                initial_stage = s
                break
        e.start(initial_stage)
