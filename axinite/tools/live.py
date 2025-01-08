import axinite.tools as axtools
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
    while t < args.limit:
        frontend[0](args.bodies, t)
        t += args.delta
    frontend[1]()