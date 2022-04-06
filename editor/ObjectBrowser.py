from tkinter import simpledialog
from typing import Optional

from editor.GraphicalList import GraphicalList


class ObjectBrowser(simpledialog.Dialog):
    """A Dialog to select objects of a given type."""

    def __init__(self, editor, t: type, target: list):
        """
        Display an object browser.

        :param editor: The window it belongs to.
        :param t: The type of objects to select.
        :param target: List to populate with selection.
        """

        self.t: type = t
        """Type to filter selectable objects."""

        self.editor = editor

        self.target: list = target
        """List to populate with selection."""

        self.list: Optional[GraphicalList] = None

        super().__init__(editor.window, title="Select objects")

    def body(self, master) -> None:
        """Construct custom dialog body."""
        self.list = GraphicalList(master)
        objs = self.editor.obj_man.get(self.t)
        for obj in objs:
            self.list.add(obj)

    def apply(self):
        """Process selection after OK was clicked."""
        for obj in self.list.selection():
            self.target.append(obj)
