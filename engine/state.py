key_stage = "current_stage"
_state: dict = {
    key_stage: None
}


def get_state():
    return _state


def check_conditions(conditions: dict):
    conditions_match = True
    for key, value in conditions.items():
        if get_state().get(key) != value:
            conditions_match = False
            break
    return conditions_match


def apply_conditions(conditions: dict):
    for key, value in conditions.items():
        get_state()[key] = value
