from copy import copy
from tkinter import ttk


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
