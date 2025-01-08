import axinite as ax
import axinite.tools as axtools
from vpython import *
import signal

def run(_args: axtools.AxiniteArgs, frontend: 'function') -> tuple[axtools.Body, ...]:
    """Load and display a simulation simultaneously. !! USE WITH CAUTION - this function has been known to have unexpected behavior !!

    Args:
        _args (axtools.AxiniteArgs): The simulation parameters.
        frontend (function): The frontend to use.

    Returns:
        tuple[axtools.Body, ...]: The bodies in the simulation
    """

    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    args.action = frontend[0]
    signal.signal(signal.SIGINT, lambda *args, **kwargs: frontend[1])
    try: bodies = ax.load(*args.unpack(), t=args.t, action=args.action, action_frequency=10)
    finally: frontend[1]()
    return bodies