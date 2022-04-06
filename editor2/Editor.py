from __future__ import annotations
from typing import Optional, Any, Callable

import tkinter as tk
from tkinter import ttk

import engine as e


def default_object(t: type):
    """
    Construct an object of the given type using "default" arguments.
    """

    if issubclass(t, e.Stage):
        stage = e.Stage("Empty room", "This is an empty room.")
        stage.actions = [default_object(e.Action)]
        stage.props = [default_object(e.Prop)]
        return stage
    elif issubclass(t, e.Action):
        return e.Action(
            "Do nothing.", "You successfully did nothing.",
            prerequisites=lambda: True,
            consequences=[default_object(e.Statement)],
            condition=[default_object(e.Statement)]
        )
    elif issubclass(t, e.Prop):
        return e.Prop("There is a thing.")
    elif issubclass(t, e.Var):
        return e.Var("A default variable")
    elif issubclass(t, e.Statement):
        return e.Statement(default_object(e.Var), "True")
    raise TypeError(f"Cannot construct default object for unknown type {t}.")


class Subscriber:

    def receive(self, other: Item):
        pass


class Item:

    def __init__(self, obj: object):
        self.obj = obj
        self.subscribers: list[Subscriber] = []

    def get_type(self):
        return self.obj.__class__

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.receive(self)

    def read(self):
        return self.obj

    def write(self, new_attributes: dict[str, Any]):
        for key, value in new_attributes.items():
            self.obj.__setattr__(key, value)
        self.notify()

    def subscribe(self, other: Subscriber):
        self.subscribers.append(other)

    def unsubscribe(self, other: Subscriber):
        self.subscribers.remove(other)


class Form:

    def __init__(self, master, t: type):
        self.attributes: dict[str, Any] = {}
        self.frame = ttk.Frame(master)
        ttk.Label(self.frame, text=f"Form for {t}").pack()

        # For each attribute add an appropriate method of input
        default_obj = default_object(t)
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
            # elif isinstance(value, list):
            #     if value:
            #         self.attributes[key] = ListView(self.frame, value[0].__class__)
            # elif isinstance(value, e.Var):
            #     self.attributes[key] = ObjectSlot(self.frame, e.Var)
            else:
                ttk.Label(self.frame, text="Cannot edit.", justify="center",
                          foreground="gray").pack()

    def show(self, obj: Item):
        for attr_name in self.attributes.keys():
            self.attributes[attr_name].set(obj.read().__getattribute__(attr_name))
        self.frame.pack()

    def read(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, container in self.attributes.items():
            result[key] = container.get()
        return result

    def hide(self):
        self.frame.pack_forget()


class ObjectManager:

    def __init__(self):
        self.objs_by_type: dict[type, list[object]] = {}

    def new(self, t: type) -> Item:
        new_obj = Item(default_object(t))
        self.objs_by_type.setdefault(t, []).append(new_obj)
        return new_obj

    def delete(self, obj: Item):
        pass

    # def update(self, obj: Item, new_attributes: dict[str, Any]):
    #     obj.write(new_attributes)

    def get(self, t: type):
        return self.objs_by_type[t]


class Editor:

    def __init__(self, master, object_manager: ObjectManager):
        self.frame = ttk.Frame(master)
        self.frame.pack()
        ttk.Label(self.frame, text="Editor").pack()

        self.form_by_type: dict[type, Form] = {}
        self.form: Optional[Form] = None
        self.opened: Optional[Item] = None
        self.obj_man: ObjectManager = object_manager

        ttk.Button(self.frame, text="Save", command=self.save).pack(side="bottom")

    def get_form(self, t: type):
        return self.form_by_type.setdefault(t, Form(self.frame, t))

    def open(self, obj: Item):
        self.close()
        self.opened = obj
        self.form = self.get_form(obj.get_type())
        self.form.show(obj)

    def save(self):
        if self.opened is not None:
            data = self.form.read()
            self.opened.write(data)
            # self.obj_man.update(self.opened, data)

    def close(self):
        if self.opened is not None:
            self.opened = None
            self.form.hide()


class ItemList(Subscriber):

    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack()

        self.items_by_id: dict[str, Item] = {}
        self.ids_by_items: dict[Item, str] = {}

        self.tree = ttk.Treeview(self.frame, columns=["Description"], height=24)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("Description", text="Description")
        self.tree.pack(side="left")

        sb = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.config(yscrollcommand=sb.set)
        sb.config(command=self.tree.yview)

    def get_id(self, obj: Item) -> str:
        return self.ids_by_items[obj]

    def get_item(self, identifier: str) -> Item:
        return self.items_by_id[identifier]

    def add(self, obj: Item):
        obj.subscribe(self)
        identifier = self.tree.insert("", "end", values=[str(obj.read())])

        self.items_by_id[identifier] = obj
        self.ids_by_items[obj] = identifier

    def _remove(self, obj_id: str):
        obj = self.get_item(obj_id)
        obj.unsubscribe(self)
        self.tree.delete(obj_id)

        del self.items_by_id[obj_id]
        del self.ids_by_items[obj]

    def remove_selection(self):
        for selected in self.tree.selection():
            self._remove(selected)

    def receive(self, other: Item):
        identifier = self.get_id(other)
        self.tree.item(identifier, values=[str(other.read())])

    def get_selection(self) -> list[Item]:
        return [self.get_item(identifier) for identifier in self.tree.selection()]

    def get_first_selected(self) -> Optional[Item]:
        try:
            return self.get_item(self.tree.selection()[0])
        except IndexError:
            return None


class Browser:

    def __init__(self, master, object_manager: ObjectManager):
        self.editor: Optional[Editor] = None
        self.obj_man: ObjectManager = object_manager

        frame = ttk.Frame(master)
        frame.pack()
        ttk.Label(frame, text="Browser").pack()

        for t in [e.Stage, e.Action, e.Statement, e.Var, e.Prop]:
            ttk.Button(frame, text=f"New {t}", command=lambda x=t: self.create(x)).pack(fill="x")

        self.item_list = ItemList(frame)

        ttk.Button(frame, text="Delete", command=self.destroy).pack()
        ttk.Button(frame, text="Edit", command=self.edit).pack()

    def set_editor(self, editor: Editor):
        self.editor = editor

    def edit(self):
        obj = self.item_list.get_first_selected()
        if obj is not None:
            self.editor.open(obj)

    def destroy(self):
        self.editor.close()
        self.item_list.remove_selection()
        # self.obj_man.delete(obj)

    def create(self, t: type):
        new_obj: Item = self.obj_man.new(t)
        self.item_list.add(new_obj)
        self.editor.open(new_obj)


class App:

    def __init__(self):
        self.window: tk.Tk = tk.Tk()
        self.window.title("Editor")
        self.window.geometry("1280x720+10+10")

        frame_browser = ttk.Frame(self.window)
        frame_browser.pack(anchor="nw", side="left")
        frame_editor = ttk.Frame(self.window)
        frame_editor.pack(anchor="nw")

        self.obj_man: ObjectManager = ObjectManager()
        browser = Browser(frame_browser, self.obj_man)
        self.editor: Editor = Editor(frame_editor, self.obj_man)
        browser.set_editor(self.editor)

    def start(self):
        self.window.mainloop()

    def read(self):
        pass

    def write(self):
        pass

    def launch_game(self):
        pass


if __name__ == '__main__':
    app = App()
    app.start()
