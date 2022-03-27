from typing import Callable, Any, Optional
from collections import defaultdict

from engine.state import check_conditions, apply_conditions


class Action:
    """
    An action can be performed if it is enabled and all the prerequisite events have been triggered.
    Once an action is performed all the effects which are events will be triggered.
    """
    on_performed = Callable[[Any, bool], None]

    def __init__(
            self,
            description: str,
            success_text: str,
            failure_text: str = "",
            auto_disable: bool = False,
            is_enabled: bool = True,
            consequences=None,
            conditions=None,
            prerequisites=None
    ):
        self.description = description
        self.success_text = success_text
        self.failure_text = failure_text
        self.prerequisites = prerequisites
        self.consequences = consequences
        self.conditions = conditions
        self.auto_disable = auto_disable
        self.is_enabled = is_enabled

    def can_attempt(self) -> bool:
        return self.is_enabled and check_conditions(self.prerequisites)

    def _can_succeed(self) -> bool:
        return check_conditions(self.conditions)

    def on_succeed(self):
        pass

    def _succeed(self):
        if self.auto_disable:
            self.is_enabled = False
        apply_conditions(self.consequences)
        self.on_succeed()
        Action.on_performed(self, True)

    def _fail(self):
        # self.fail_event.trigger()
        Action.on_performed(self, False)

    def attempt(self):
        if self._can_succeed():
            self._succeed()
        else:
            self._fail()
