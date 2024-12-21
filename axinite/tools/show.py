import axinite as ax
from vpython import *
import axinite.tools as axtools
from itertools import cycle
import vpython as vp

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(_args, frontend):
    """Statically display a preloaded simulation."""

    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
        args.retain = 200

    for body in args.bodies:
        frontend(body)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass