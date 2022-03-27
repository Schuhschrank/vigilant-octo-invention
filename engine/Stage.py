from engine.Action import Action


class Stage:
    """A state in which only a certain set of actions can be performed."""

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.actions: list[Action] = []

    def add_actions(self, additional_actions: list[Action]):
        """Add actions which shall be performable within this stage."""
        self.actions.extend(additional_actions)

    def __iadd__(self, other):
        """Calls add_actions."""
        self.add_actions(other)
        return self

    def get_performable_actions(self) -> list[Action]:
        """Returns a list of actions which can currently be attempted."""
        return [a for a in self.actions if a.can_attempt()]
