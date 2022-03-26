from typing import Callable
from typing import Any


class Event:
    on_triggered: Callable[[Any], None] = lambda x: print("Event triggered: " + str(x))

    def __init__(self, description: str):
        self.description: str = description
        self.was_triggered: bool = False

    def trigger(self) -> None:
        self.was_triggered = True
        Event.on_triggered(self)

    def __str__(self):
        return self.description


def were_triggered(events: list[Event]) -> bool:
    result = True
    for e in events:
        if not e.was_triggered:
            result = False
            break
    return result
