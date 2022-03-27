from engine.Stage import Stage
from engine.state import state, key_stage
from typing import Optional


def stage(new_stage: Optional[Stage] = None) -> Optional[Stage]:
    """If an argument is given, it will change the stage, else it returns the current stage."""
    if new_stage is None:
        return state[key_stage]
    else:
        state[key_stage] = new_stage
