import axinite as ax
import axinite.tools as axtools
from vpython import *

def run(_args: axtools.AxiniteArgs, frontend):
    """Load and display a simulation simultaneously."""

    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    args.action = frontend[0]
    try: ax.load_legacy(*args.unpack(), t=args.t, action=args.action)
    finally: frontend[1]()