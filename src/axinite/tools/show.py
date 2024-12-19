import axinite as ax
from vpython import *
import axinite.tools as axtools
from itertools import cycle
import vpython as vp

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(_args, frontend):
    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
        args.retain = 200

    while args.t < args.limit:
        frontend(args.t, bodies=args.bodies)
        args.t += args.delta