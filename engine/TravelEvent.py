from engine.Event import Event
from engine.Stage import Stage
from engine.current_stage import *


class TravelEvent(Event):
    """When triggered we will travel to the stage given as an argument."""

    def __init__(self, description: str, new_stage: Stage):
        super().__init__(description)
        self.new_stage: Stage = new_stage

    def on_trigger(self) -> None:
        """Perform travel."""
        set_stage(self.new_stage)
