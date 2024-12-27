import axinite as ax
import axinite.tools as axtools
from axinite.tools import AxiniteArgs
import json
from numba import jit
_jit = jit

def load(args: AxiniteArgs, path: str = "", dont_change_args: bool = False, jit: bool = True, verbose: bool = True):
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
    
    #if args.action == None: args.action = lambda t, **kwargs: print(f"Timestep {t} ({((t / args.limit) * 100).value:.2f}% complete)", end="\r")
    if args.backend == None: args.backend = ax.euler_backend

    bodies = ax.load(*args.unpack(), t=args.t, modifier=args.modifier, action=args.action)
    if verbose: print(f"Finished with {len(bodies[0].r)} timesteps")

    _bodies = []
    for i, body in enumerate(bodies):
        _bodies.append(args.bodies[i])
        for j, r in body.r.items():
            _bodies[i].r[j] = r
            _bodies[i].v[j] = body.v[j]
    if path == "": 
        if not dont_change_args:
            args.t = args.limit
            args.bodies = _bodies
        return _bodies
    else: 
        with open(path, 'w+') as f:
            data = {
                "name": args.name,
                "delta": args.delta.value,
                "limit": args.limit.value,
                "t": args.t.value,
                "radius_multiplier": args.radius_multiplier,
                "bodies": []
            }

            for body in _bodies: 
                body_data = {
                    "name": body.name,
                    "mass": body.mass.value,
                    "radius": body.radius.value,
                    "r": {k: [v.x.value, v.y.value, v.z.value] for k, v in body.r.items()},
                    "v": {k: [v.x.value, v.y.value, v.z.value] for k, v in body.v.items()}
                }
                if body.color != None:
                    body_data["color"] = body.color
                if body.retain != None:
                    body_data["retain"] = body.retain
                if body.light != None:
                    body_data["light"] = body.light

                data["bodies"].append(body_data)

            if args.radius_multiplier is not None:
                data["radius_multiplier"] = args.radius_multiplier

            if args.rate is not None:
                data["rate"] = args.rate

            if args.retain is not None:
                data["retain"] = args.retain
            
            if args.frontend_args != {}:
                data["frontend_args"] = args.frontend_args

            json.dump(data, f, indent=4)
            if not dont_change_args:
                args.t = args.limit
                args.bodies = _bodies
            return _bodies