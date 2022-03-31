def _apply_consequences(consequences):
    """Apply the given consequences."""

    if consequences is None:
        return
    for variable, value in consequences:
        if hasattr(variable, "description"):
            variable.description = value
        else:
            variable.value = value


class Action:
    """An action changes the state of the game.

    An action can be attempted if it is enabled and all the prerequisites are true.
    An action succeeds if all the conditions are true, then all the statements defined in the
    consequences will be applied.
    """

    def __init__(self, description, success_text, failure_text="That didn't work.",
                 auto_disable=False, is_enabled=True, consequences=None, condition=lambda: True,
                 prerequisites=lambda: True):
        """Construct and return an action.

        :param description: Describes to the player what the action is.
        :param success_text: Displayed if the action is performed successfully.
        :param failure_text: Displayed if the action is failed to perform.
        :param auto_disable: Should the action be hidden after first success?
        :param is_enabled: Should the action be shown and possible to succeed?
        :param consequences: A list that defines the consequences of a successful attempt. Either
         use a tuple of a Var and a value (Var(), False) or a Prop and a string (Prop(), "").
        :param condition: A list of conditions that must be true in order for an attempt to succeed.
         Defined as tuples like the first described for consequences.
        :param prerequisites: A list of conditions that must be true in order for the action to be
        shown to the player. Defined the same as conditions.
        """

        self.description = description
        self.success_text = success_text
        self.failure_text = failure_text
        self.prerequisites = prerequisites
        self.consequences = consequences
        self.conditions = condition
        self.auto_disable = auto_disable
        self.is_enabled = is_enabled

    def can_attempt(self) -> bool:
        """Return whether an action can be attempted; will be hidden if not."""

        return self.is_enabled and self.prerequisites()

    def on_succeed(self):
        """Process a successful attempt. Override this for any behaviour."""

        pass

    def attempt(self) -> bool:
        """
        Attempt to perform this action.

        If the conditions are met the consequences will be applied, this action disabled if
        appropriate and on_succeed() called.
        :return: Whether the attempt was successful.
        """

        assert self.can_attempt()
        if self.conditions():
            self.is_enabled = not self.auto_disable
            _apply_consequences(self.consequences)
            self.on_succeed()
            return True
        return False

    def __repr__(self):
        return f"{self.description}"
