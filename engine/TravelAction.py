from engine.Action import Action
from engine.Stage import Stage, stage


class TravelAction(Action):
    """A subclass of Action that enables travel to a given stage."""

    def __init__(self, new_stage: Stage, description=None, success_text=None,
                 failure_text: str = "", auto_disable: bool = False, is_enabled: bool = True,
                 consequences=None, condition=lambda: True, prerequisites=lambda: True):
        """Construct and return a travel action.

        :param new_stage: The stage to travel to when this action is performed successfully.
        """

        if description is None:
            description = f"Enter the {new_stage.name}."
        if success_text is None:
            success_text = f"You entered the {new_stage.name}."
        self.new_stage = new_stage
        super().__init__(description=description, success_text=success_text,
                         failure_text=failure_text, auto_disable=auto_disable,
                         is_enabled=is_enabled, consequences=consequences, condition=condition,
                         prerequisites=prerequisites)

    def on_succeed(self):
        """Perform travel."""

        stage(self.new_stage)
