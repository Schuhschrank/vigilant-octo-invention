from engine.Stage import Stage
from typing import Optional

_stage = None


def stage(new_stage: Optional[Stage] = None) -> Optional[Stage]:
    """If an argument is given, it will change the stage, else it returns the current stage."""
    global _stage
    if new_stage is None:
        return _stage
    else:
        _stage = new_stage
