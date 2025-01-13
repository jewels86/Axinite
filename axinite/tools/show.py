from vpython import *
import axinite.tools as axtools
from itertools import cycle
import signal

def show(_args: axtools.AxiniteArgs, frontend: 'function') -> None:
    """Statically display the bodies in the simulation.

    Args:
        _args (axtools.AxiniteArgs): The simulation parameters.
        frontend (function): The frontend function.
    """

    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
        args.retain = 200

    for body in args.bodies:
        frontend[0](body)

    if frontend[1] != None: 
        frontend[1]()

    signal.signal(signal.SIGINT, lambda *args, **kwargs: frontend[2])