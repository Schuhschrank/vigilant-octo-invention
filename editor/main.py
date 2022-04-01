from typing import Optional, Callable, Any
from copy import copy

import tkinter as tk
from tkinter import ttk, simpledialog

import engine as e

root = tk.Tk()
root.title("Editor")
root.geometry("1600x900+10+10")


def default_object(t: type) -> object:
    """
    Construct an object of the given type using "default" arguments.

    :param t: Type of the object to be constructed.
    :return: Object constructed using "default" arguments, or None if there are no definitions for
     the type.
    """
    if issubclass(t, e.Stage):
        return e.Stage("Empty room", "This is an empty room.")
    elif issubclass(t, e.Action):
        return e.Action("Do nothing.", "You successfully did nothing.")
    elif issubclass(t, e.Prop):
        return e.Prop("There is a thing.")
    return None


class GraphicalList:

    def __init__(self, master):
        self.objects: dict[str, object] = {}
        self.identifiers: dict[object, str] = {}
        frame = ttk.Frame(master)
        frame.pack()
        self.treeview = ttk.Treeview(frame, columns=["0", "1"], show="headings")
        self.treeview.heading(0, text="Type")
        self.treeview.heading(1, text="Description")
        self.treeview.pack()

    @staticmethod
    def get_values(obj: object):
        return [str(obj.__class__), str(obj)]

    def add(self, obj: object):
        if obj not in self.identifiers:
            identifier = self.treeview.insert("", "end", values=self.get_values(obj))
            self.objects[identifier] = obj
            self.identifiers[obj] = identifier

    def update(self, obj: object):
        identifier = self.identifiers[obj]
        self.treeview.item(identifier, values=self.get_values(obj))

    def remove(self, obj):
        identifier = self.identifiers[obj]
        self.treeview.delete(identifier)
        del self.objects[identifier]
        del self.identifiers[obj]

    def selection(self):
        return [self.objects[identifier] for identifier in self.treeview.selection()]

    def get(self):
        return list(self.objects.values())

    def set(self, objs):
        current_objs = copy(self.get())
        for obj in current_objs:
            self.remove(obj)
        for obj in objs:
            self.add(obj)


class ListView:

    def __init__(self, master, t: type):
        self.t: type = t

        # UI
        self.frame = ttk.Frame(master)
        self.frame.pack()
        ttk.Label(self.frame, text="List", font=14).pack()
        self.list = GraphicalList(self.frame)
        button_frame = ttk.Frame(self.frame)
        button_frame.pack()
        ttk.Button(button_frame, text="Add", command=self.select).pack(side="left")
        ttk.Button(button_frame, text="Remove selection", command=self.remove).pack(side="left")

    def select(self):
        selection = []
        ObjectBrowser(root, self.t, selection)
        for s in selection:
            self.add(s)

    def add(self, obj: object):
        self.list.add(obj)

    def remove(self):
        for selection in self.list.selection():
            self.list.remove(selection)

    def get(self):
        return self.list.get()

    def set(self, items):
        self.list.set(items)


class ObjectManager:
    """Keeps track of objects.

    Enables access to all objects of a certain type that were created with this manager.
    """

    def __init__(self):
        self.object_lists: dict[type, list] = {}
        """For each type holds a list of all the objects of that type."""

        self.frame = ttk.Frame(root, padding=16, relief=tk.GROOVE)
        self.frame.pack(side="left", anchor="nw")
        ttk.Label(self.frame, text="Objects", font=16).pack()
        self.list = GraphicalList(self.frame)
        ttk.Button(self.frame, text="Edit", command=self.edit).pack()
        ttk.Button(self.frame, text="Delete", command=self.delete).pack()

    def new(self, t: type):
        """Construct an object of the given type."""
        new_obj = default_object(t)
        self.object_lists.setdefault(t, []).append(new_obj)
        self.list.add(new_obj)
        return new_obj

    def internal_delete(self, obj: object = None):
        """Forget the given object, do not actually delete it."""
        self.object_lists[obj.__class__].remove(obj)

    def delete(self):
        """Delete the selected object."""
        try:
            obj = self.list.selection()[0]
            get_form(obj.__class__).unload()
            self.list.remove(obj)
            self.internal_delete(obj)
        except IndexError:
            pass

    def get(self, t: type) -> list:
        """Get all objects of the given type."""
        return self.object_lists.setdefault(t, [])

    def update(self, obj: object):
        self.list.update(obj)

    def edit(self):
        try:
            obj = self.list.selection()[0]
            get_form(obj.__class__).load(obj)
        except IndexError:
            pass


obj_man = ObjectManager()
"""The only ObjectManager instance."""


class ObjectBrowser(simpledialog.Dialog):
    """A Dialog to select objects of a given type."""

    def __init__(self, parent, t: type, target: list):
        """
        Display an object browser.

        :param parent: The window it belongs to.
        :param t: The type of objects to select.
        :param target: List to populate with selection.
        """

        self.t: type = t
        """Type to filter selectable objects."""

        self.target: list = target
        """List to populate with selection."""

        self.list: Optional[GraphicalList] = None

        super().__init__(parent, title="Select objects")

    def body(self, master) -> None:
        """Construct custom dialog body."""
        self.list = GraphicalList(master)
        objs = obj_man.get(self.t)
        for obj in objs:
            self.list.add(obj)

    def apply(self):
        """Process selection after OK was clicked."""
        for obj in self.list.selection():
            self.target.append(obj)


class Form:
    """Graphical form to construct/edit objects of a given type."""

    instances = {}

    def __init__(self, t: type):
        """
        Construct a form tailored to the given type.

        :param t: Type to tailor to.
        """

        self.type: type = t

        self.attributes: dict = {}
        """Maps attributes to the appropriate input variable."""

        self.loaded_object: object = None
        """Object currently loaded for editing."""

        default_obj = default_object(t)
        """Used for generating the form according to its attributes."""

        # UI generation

        self.frame: ttk.Frame = ttk.Frame(root, relief=tk.GROOVE, padding=32)
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
                self.attributes[key] = ListView(self.frame, e.Action)
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
            self.loaded_object = obj_man.new(self.type)
        # Override attributes
        for key, value in self.attributes.items():
            self.loaded_object.__setattr__(key, value.get())
        obj_man.update(self.loaded_object)
        self.loaded_object = None


def get_form(t: type) -> Form:
    return Form.instances[t]


# Forms
stage_form = Form(e.Stage)
action_form = Form(e.Action)
prop_form = Form(e.Prop)

root.mainloop()
