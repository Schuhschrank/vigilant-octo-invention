from tkinter import ttk

from editor.ObjectBrowser import ObjectBrowser


class ObjectSlot:
    """Holds an object and enables finding one."""

    def __init__(self, master, t: type):
        self.obj: object = None
        self.t: type = t

        self.frame = ttk.Frame(master)
        self.frame.pack()
        self.label = ttk.Label(self.frame)
        self.label.pack(side="left")
        self.select_button = ttk.Button(self.frame, text="Select", command=self.select)
        self.select_button.pack(side="left")

    def select(self):
        target = []
        ObjectBrowser(self.frame, self.t, target)
        self.set(target[0])

    def get(self):
        return self.obj

    def set(self, obj):
        self.obj = obj
        self.label.configure(text=str(self.obj))