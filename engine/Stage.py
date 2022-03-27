from engine.Action import Action
from tkinter import PhotoImage, Image


class Stage:
    """A state in which only a certain set of actions can be performed."""

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.image: Image = PhotoImage(file="./engine/default_image.png")
        self.actions: list[Action] = []

    def set_image(self, path: str):
        """Example for path: ./engine/default_image.png"""
        self.image = PhotoImage(file=path)

    def add_actions(self, additional_actions: list[Action]):
        """Add actions which shall be performable within this stage."""
        self.actions.extend(additional_actions)
