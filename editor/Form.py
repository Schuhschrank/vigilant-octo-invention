import tkinter as tk
from tkinter import ttk

import engine as e
from editor.ListView import ListView
from editor.ObjectSlot import ObjectSlot
from editor.default_objects import default_object


class Form:
    """Graphical form to construct/edit objects of a given type."""

    instances = {}

    def __init__(self, master, obj_man, t: type):
        """
        Construct a form tailored to the given type.

        :param t: Type to tailor to.
        """

        self.obj_man = obj_man

        self.type: type = t

        self.attributes: dict = {}
        """Maps attributes to the appropriate input variable."""

        self.loaded_object: object = None
        """Object currently loaded for editing."""

        default_obj = default_object(t)
        """Used for generating the form according to its attributes."""

        # UI generation

        self.frame: ttk.Frame = ttk.Frame(master, relief=tk.GROOVE, padding=32)
        self.frame.pack(side="left", anchor="nw")

        # Title
        ttk.Label(self.frame, text=f"Edit {str(self.type)}", font=16).pack()

        # For each attribute add an appropriate method of input
        for key, value in default_obj.__dict__.items():

            # Attribute name label
            attr_name = key.replace("_", " ")
            attr_name = attr_name.capitalize()
            label = ttk.Label(self.frame, text=attr_name)
            label.pack(anchor="w")

            # Setup input
            if isinstance(value, str):
                string_var = tk.StringVar(value=value)
                self.attributes[key] = string_var
                ttk.Entry(self.frame, textvariable=string_var).pack(fill="x")
            elif isinstance(value, bool):
                bool_var = tk.BooleanVar(value=value)
                self.attributes[key] = bool_var
                ttk.Checkbutton(self.frame, variable=bool_var).pack(fill="x")
            elif isinstance(value, list):
                if value:
                    self.attributes[key] = ListView(self.frame, value[0].__class__)
            elif isinstance(value, e.Var):
                self.attributes[key] = ObjectSlot(self.frame, e.Var)
            else:
                ttk.Label(self.frame, text="Cannot edit.", justify="center",
                          foreground="gray").pack()

        ttk.Button(self.frame, text="Save object", command=self.save).pack()
        Form.instances[self.type] = self

    def load(self, obj: object) -> None:
        """
        Holds the object for modification and fills the form with the object's attribute's values.

        :param obj: Object to load.
        """

        assert isinstance(obj, self.type)
        self.loaded_object = obj
        # Fill out form
        for key in self.attributes.keys():
            self.attributes[key].set(obj.__getattribute__(key))

    def unload(self):
        self.loaded_object = None

    def save(self):
        """Save changes and unload, or create new object.

        Override loaded object's attributes with user input, or construct new object with user input
        if none is loaded.
        """

        if self.loaded_object is None:
            self.loaded_object = self.obj_man.create(self.type)
        # Override attributes
        for key, value in self.attributes.items():
            self.loaded_object.__setattr__(key, value.get())
        self.obj_man.update(self.loaded_object)
        self.loaded_object = None
