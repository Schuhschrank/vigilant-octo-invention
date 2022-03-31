from typing import Optional, Callable, Any, Type
from copy import copy

import tkinter as tk
from tkinter import ttk

import engine as e

root = tk.Tk()
root.title("Editor")
root.geometry("1280x720+100+100")

add_object_to_list: Optional[Callable[[object], None]] = None
update_object_in_list: Optional[Callable[[object], None]] = None


class Form:
    instances = {}

    def __init__(self, default_obj: object):
        self.frame: ttk.Frame = ttk.Frame(root, relief=tk.GROOVE, padding=32)
        self.frame.pack()
        self.entries: dict = {}
        self.loaded_object: object = None
        self.default_obj: object = default_obj
        self.type: type = default_obj.__class__
        ttk.Label(self.frame, text=f"Edit {str(self.type)}", font=16).pack()
        for key, value in default_obj.__dict__.items():
            if isinstance(value, str):
                label = ttk.Label(self.frame, text=key)
                label.pack(anchor="w")
                string_var = tk.StringVar(value=value)
                self.entries[key] = string_var
                ttk.Entry(self.frame, textvariable=string_var).pack(fill="x")
            elif isinstance(value, bool):
                label = ttk.Label(self.frame, text=key)
                label.pack(anchor="w")
                bool_var = tk.BooleanVar(value=value)
                self.entries[key] = bool_var
                rb = ttk.Checkbutton(self.frame, variable=bool_var)
                rb.pack(fill="x")
        ttk.Button(self.frame, text="Save object", command=self.save).pack()
        Form.instances[self.type] = self

    def load(self, obj: object):
        assert isinstance(obj, self.type)
        self.loaded_object = obj
        # Fill out form
        for key in self.entries.keys():
            self.entries[key].set(obj.__getattribute__(key))

    def save(self):
        if self.loaded_object is None:
            self.loaded_object = copy(self.default_obj)
            add_object_to_list(self.loaded_object)
        for key, value in self.entries.items():
            self.loaded_object.__setattr__(key, value.get())
        update_object_in_list(self.loaded_object)
        self.loaded_object = None


def get_form(t: type) -> Form:
    return Form.instances[t]


class ListElement:
    instances = {}

    def __init__(self, frame: ttk.Frame, obj: object):
        self.obj: obj = obj
        self.label = ttk.Label(frame, text=str(obj))
        self.label.pack()
        self.button_edit = ttk.Button(frame, text="Edit stage", command=self.edit)
        self.button_edit.pack()
        self.button_del = ttk.Button(frame, text="Delete stage", command=self.delete)
        self.button_del.pack()
        ListElement.instances[self.obj] = self

    def edit(self):
        get_form(self.obj.__class__).load(self.obj)

    def update(self):
        self.label.configure(text=str(self.obj))

    def delete(self):
        self.label.destroy()
        self.button_edit.destroy()
        self.button_del.destroy()
        del ListElement.instances[self.obj]
        del self


def get_object(obj: object) -> ListElement:
    return ListElement.instances[obj]


class List:

    def __init__(self):
        self.frames = {}

    def add_entry(self, obj: object):
        obj_class: type = obj.__class__
        if obj_class not in self.frames.keys():
            frame = ttk.Frame(root, relief=tk.GROOVE, padding=16)
            frame.pack()
            ttk.Label(frame, text=f"List of all the {str(obj_class)}", font=16).pack()
            self.frames[obj_class] = frame
        ListElement(self.frames[obj_class], obj)


object_list = List()


def add_object_impl(obj: object):
    object_list.add_entry(obj)


def update_object_impl(obj: object):
    get_object(obj).update()


# noinspection PyRedeclaration
add_object_to_list = add_object_impl
# noinspection PyRedeclaration
update_object_in_list = update_object_impl

default_stage = e.Stage("An empty room", "The room is empty.")
stage_form = Form(default_stage)

default_action = e.Action("Do nothing.", "You successfully did nothing.")
action_form = Form(default_action)

root.mainloop()
