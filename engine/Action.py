from engine.Event import Event
from engine.Event import were_triggered


class Action:
    """
    An action can be performed if it is enabled and all the prerequisite events have been triggered.
    Once an action is performed all the effects which are events will be triggered.
    """
    on_performed = None

    def __init__(self, description: str, consequences: list[Event], auto_disable=False):
        self.prerequisites: list[Event] = []
        self.consequences: list[Event] = consequences
        self.conditions: list[Event] = []
        self.fail_event: Event = Event("Action failed.")
        self.is_enabled = True
        self.auto_disable = auto_disable
        self.description = description

    def can_attempt(self):
        if not self.is_enabled:
            return False
        return were_triggered(self.prerequisites)

    def _can_succeed(self):
        return were_triggered(self.conditions)

    def _succeed(self):
        if self.auto_disable:
            self.is_enabled = False
        for e in self.consequences:
            e.trigger()
        Action.on_performed()

    def _fail(self):
        self.fail_event.trigger()

    def attempt(self):
        if self._can_succeed():
            self._succeed()
        else:
            self._fail()
