import axinite as ax
import axinite.tools as axtools
from vpython import *
from itertools import cycle
import astropy.units as u

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(args: axtools.AxiniteArgs, frontend):
    """Watch a preloaded simulation live."""
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    t = 0 * u.s
    while t < args.limit:
        frontend(t, bodies=args.bodies)
        t += args.delta