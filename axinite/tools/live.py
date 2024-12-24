import axinite as ax
import axinite.tools as axtools
from vpython import *
from itertools import cycle
import astropy.units as u

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(args: axtools.AxiniteArgs, frontend: function) -> None:
    """Watch a preloaded simulation live.

    Args:
        args (axtools.AxiniteArgs): The arguments for the simulation.
        frontend (function): The frontend to use.
    """
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    t = 0 * u.s
    try:
        while t < args.limit:
            frontend[0](t, bodies=args.bodies)
            t += args.delta
    finally: frontend[1]()