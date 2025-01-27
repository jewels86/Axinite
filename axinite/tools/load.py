import axinite as ax
import axinite.tools as axtools
import json
from numba import jit

def load(args: axtools.AxiniteArgs, path: str = "", dont_change_args: bool = False, verbose: bool = False):
    """Preloads a simulation.

    Args:
        args (AxiniteArgs): An AxiniteArgs object containing simulation parameters.
        path (str, optional): The path to dump the computed simulation to. Defaults to "", which skips data dumping.
        dont_change_args (bool, optional): True if the load function should take care not to edit the args object. Defaults to False.
        verbose (bool, optional): Whether the load function should print to console. Defaults to False.

    Returns:
        list[axtools.Body]: A list of Body objects containing the preloaded simulation data.
    """
    
    if args.action == None: 
        ntotal = args.limit / args.delta

        @jit(nopython=False)
        def default_action(bodies, t, limit, delta, n): print("Timestep", n, "/", ntotal, "(", round(t / limit * 100, 2), "\b% )\033[F")

        args.action = default_action if verbose else None
        args.action_frequency = 200
    if args.backend == None: args.backend = ax.verlet_backend
    if verbose: print(f"Initializing system...")
    bodies = ax.load(*args.unpack(), t=args.t, modifier=args.modifier, action=args.action, action_frequency=args.action_frequency)
    if verbose: 
        print(f"Finished with {bodies[0]._inner['r'].shape[0]} timesteps \033[K")
        print(f"Synchronizing inner and outer bodies...")

    _bodies = []
    for i, body in enumerate(bodies):
        _bodies.append(axtools.Body(body.name, body.mass, args.limit, args.delta, position=body.r(0), velocity=body.v(0)))
        _bodies[i].retain = args.bodies[i].retain
        _bodies[i].color = args.bodies[i].color
        _bodies[i].light = args.bodies[i].light
        _bodies[i].radius = args.bodies[i].radius
        _bodies[i].radius_multiplier = args.bodies[i].radius_multiplier

        _bodies[i]._inner = body._inner
    
    if not dont_change_args:
        args.t = args.limit
        args.bodies = _bodies
    if path == "":
        return _bodies
    else: 
        if verbose: print(f"Saving system data to file...")
        axtools.save(args, path)
        if verbose: print(f"Finished saving system data to file")
        return _bodies