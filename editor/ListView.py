from tkinter import ttk

from editor.GraphicalList import GraphicalList
from editor.ObjectBrowser import ObjectBrowser


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
        ObjectBrowser(self.frame, self.t, selection)
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
