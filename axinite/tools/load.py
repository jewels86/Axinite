import axinite as ax
import axinite.tools as axtools
from axinite.tools import AxiniteArgs
import json
from numba import jit

def load(args: AxiniteArgs, path: str = "", dont_change_args: bool = False, verbose: bool = True):
    """Preloads a simulation.

    Args:
        args (AxiniteArgs): An AxiniteArgs object containing simulation parameters.
        path (str, optional): The path to dump the computed simulation to. Defaults to "", which skips data dumping.
        dont_change_args (bool, optional): True if the load function should take care not to edit the args object. Defaults to False.
        jit (bool, optional): Whether JIT should be used. Defaults to True.
        verbose (bool, optional): Whether the load function should print to console. Defaults to True.

    Returns:
        list[axtools.Body]: A list of Body objects containing the preloaded simulation data.
    """
    
    if args.action == None: 
        delta = args.delta.value
        limit = args.limit.value

        @jit(nopython=False)
        def default_action(bodies, t, limit, delta): print("Timestep", round(t / delta), "(", round(t / limit * 100, 2), "\b% )")

        args.action = default_action if verbose else None
        args.action_frequency = 200
    if args.backend == None: args.backend = ax.verlet_backend

    bodies = ax.load(*args.unpack(), t=args.t, modifier=args.modifier, action=args.action)
    if verbose: print(f"Finished with {len(bodies[0].r)} timesteps")

    _bodies = []
    for i, body in enumerate(bodies):
        _bodies.append(args.bodies[i])
        for j, r in body.r.items():
            _bodies[i].r[j] = r
            _bodies[i].v[j] = body.v[j]
    
    if not dont_change_args:
        args.t = args.limit
        args.bodies = _bodies
    if path == "":
        return _bodies
    else: 
        axtools.save(args, path)
        return _bodies