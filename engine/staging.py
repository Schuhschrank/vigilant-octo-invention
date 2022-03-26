from engine.Stage import Stage
from engine.state import get_state, key_stage


def set_stage(new_stage: Stage):
    """Changes the currently active stage."""
    get_state()[key_stage] = new_stage


def get_stage() -> Stage:
    """Returns the currently active stage."""
    return get_state()[key_stage]
