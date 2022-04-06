class Var:

    def __init__(self, name: str, initial_value=None):
        self.name: str = name
        self.value: str = initial_value

    def __repr__(self):
        return self.name


def new_variable(initial_value=None, name: str = "Some variable"):
    if initial_value is not None:
        return Var(name, initial_value)
    return Var(name)

