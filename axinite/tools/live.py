import axinite as ax
import axinite.tools as axtools
from vpython import *
from itertools import cycle

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(_args: axtools.AxiniteArgs, frontend=axtools.vpython_frontend):
    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200


    args.action = frontend(args)
    ax.load(*args.unpack(), t=args.t)