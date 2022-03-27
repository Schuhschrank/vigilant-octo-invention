from engine.framework import *
from engine.GUI import start as _start_gui


def start(initial_stage: Stage):
    stage(initial_stage)
    _start_gui()
