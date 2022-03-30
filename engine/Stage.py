from tkinter import PhotoImage

from engine.Action import Action
from engine.settings import image_folder_path

from typing import Optional


class Stage:
    """A stage contains props and allows actions.

    A stage represents a scene of your game, e.g., a bedroom with a bed (prop) and the option to
    jump on the bed (action).
    """

    def __init__(self, name: str, description: str, image_name: str = ""):
        """Construct and return a stage.

        :param name: Name of the stage (e.g. Bedroom)
        :param description: Description of the stage excluding the descriptions of the props.
        :param image_name: Name of the file that is the image which depicts the stage and is
         displayed to the player (e.g. "default_image.png").
        """

        self.name: str = name
        self._description: str = description
        self.image = PhotoImage(file=image_folder_path + image_name) if image_name else None
        self.actions: list[Action] = []
        self.actors = None

    @property
    def description(self):
        """Return an up-to-date description of the stage and its props.

        Example "The stage is empty. There is a closed door. You see a bed in the corner of the
        room."
        """

        texts = [self._description]
        if self.actors is not None:
            texts.extend([str(a) for a in self.actors])
        return " ".join(texts)

    def set_image(self, file_name: str):
        """Set the stage's image that is displayed to the player.

        Searches the "images" folder in the directory of your main file (e.g. "main.py").
        :param file_name: Name of the file that is the desired image (e.g. "default_image.png")
        """

        self.image = PhotoImage(file=image_folder_path + file_name)

    def add_actions(self, additional_actions: list[Action]):
        """Add actions to this stage."""

        self.actions.extend(additional_actions)


_stage = None


def stage(new_stage=None) -> Optional[Stage]:
    """Get or set the current stage.

    :param new_stage: Will be set as the current stage if not None.
    :return: Current stage if no argument is passed else None.
    """

    global _stage
    if new_stage is None:
        return _stage
    else:
        _stage = new_stage
