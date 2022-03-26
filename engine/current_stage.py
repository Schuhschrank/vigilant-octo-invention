from engine.Stage import Stage

_current_stage: Stage = Stage("This is an empty stage.")
"""Do not operate on this directly. Use set_stage or get_stage instead."""


def set_stage(new_stage: Stage):
    """Changes the currently active stage."""
    global _current_stage
    _current_stage = new_stage


def get_stage() -> Stage:
    """Returns the currently active stage."""
    return _current_stage
