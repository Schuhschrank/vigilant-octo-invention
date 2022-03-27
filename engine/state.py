key_stage = "current_stage"
state: dict = {
    key_stage: "None"
}

num_keys = 0


def add_var(value=None):
    global num_keys
    state[num_keys] = value
    num_keys += 1
    return num_keys - 1


def check_conditions(conditions: dict):
    conditions_match = True
    for key, value in conditions.items():
        if state.get(key) != value:
            conditions_match = False
            break
    return conditions_match


def apply_conditions(conditions: dict):
    for key, value in conditions.items():
        state[key] = value
