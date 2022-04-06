import engine as e


def default_object(t: type):
    """
    Construct an object of the given type using "default" arguments.

    :param t: Type of the object to be constructed.
    :return: Object constructed using "default" arguments, or None if there are no definitions for
     the type.
    """
    if issubclass(t, e.Stage):
        stage = e.Stage("Empty room", "This is an empty room.")
        stage.actions = [default_object(e.Action)]
        stage.props = [default_object(e.Prop)]
        return stage
    elif issubclass(t, e.Action):
        return e.Action(
            "Do nothing.", "You successfully did nothing.",
            prerequisites=lambda: True,
            consequences=[default_object(e.Statement)],
            condition=[default_object(e.Statement)]
        )
    elif issubclass(t, e.Prop):
        return e.Prop("There is a thing.")
    elif issubclass(t, e.Var):
        return e.Var("A default variable")
    elif issubclass(t, e.Statement):
        return e.Statement(default_object(e.Var), "True")
    raise TypeError(f"Cannot construct default object for unknown type {t}.")
