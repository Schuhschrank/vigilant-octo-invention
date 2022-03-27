from engine.framework import *
from engine.GUI import start as _start_gui


class Var:

    def __init__(self, initial_value=None):
        self.value = initial_value

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other


def start(initial_stage: Stage):
    stage(initial_stage)
    _start_gui()
