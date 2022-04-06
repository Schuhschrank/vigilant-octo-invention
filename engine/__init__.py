from engine.framework import *
from engine.GUI import init as _start_gui, start_gui
import engine.settings


def init():
    _start_gui("My game")


def start(initial_stage: Stage):
    """
    Start the game.

    Any code after this call is executed once the game is ended.

    :param initial_stage: The stage to start with.
    """

    stage(initial_stage)
    start_gui()
