import axinite.tools as axtools
import axinite as ax
import astropy.units as u

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

    t = 0 * u.s
    bodies = ax.create_jit_bodies(args.bodies, args.limit, args.delta)
    while t < args.limit:
        frontend[0](bodies, t, limit=args.limit, delta=args.delta, n=int(t.value / args.delta.value))
        t += args.delta
    frontend[1]()