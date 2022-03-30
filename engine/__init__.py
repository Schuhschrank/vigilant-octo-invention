from engine.framework import *
from engine.GUI import start as _start_gui
import engine.settings


class Var:

    def __init__(self, initial_value=None):
        self.value = initial_value


def new_variable(initial_value=None):
    return Var(initial_value)


def new_variables(*initial_values):
    if len(initial_values) < 1:
        return Var(None)
    if len(initial_values) == 1:
        return Var(initial_values[0])
    t = ()
    for v in initial_values:
        t = t + tuple([Var(v)])
    return t


def start(initial_stage: Stage, game_name="My game"):
    """Start the game.

    Any code after a call to this is executed after the game ended.
    :param initial_stage: The stage with which the game should start.
    :param game_name: The name of the game. It's displayed in the title bar of the window.
    """

    stage(initial_stage)
    _start_gui(game_name)
