import tkinter as tk
from tkinter import ttk

from editor.GraphicalList import GraphicalList
from editor.get_form import get_form
from editor.default_objects import default_object


class ObjectManager:
    """Keeps track of objects.

    Enables access to all objects of a certain type that were created with this manager.
    """

    def __init__(self, master):
        self.object_lists: dict[type, list] = {}
        """For each type holds a list of all the objects of that type."""

        self.frame = ttk.Frame(master, padding=16, relief=tk.GROOVE)
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
