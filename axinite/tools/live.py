import axinite.tools as axtools
import axinite as ax

def live(args: axtools.AxiniteArgs, frontend: 'function') -> None:
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

    t = 0
    inner = ax.get_inner_bodies(args.bodies)
    while t < args.limit:
        frontend[0](inner, t, limit=args.limit, delta=args.delta, n=int(t / args.delta))
        t += args.delta
    frontend[1]()