from engine.Action import Action


class Stage:

    def __init__(self, description: str, actions: list[Action]):
        self.description: str = description
        self.actions: list[Action] = actions

    def get_performable_actions(self) -> list[Action]:
        return [a for a in self.actions if a.can_attempt()]
