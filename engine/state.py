def check_conditions(conditions):
    if conditions is None:
        return True
    conditions_match = True
    for variable, value in conditions:
        if variable != value:
            conditions_match = False
            break
    return conditions_match


def apply_conditions(conditions):
    if conditions is None:
        return
    for variable, value in conditions:
        variable.value = value
