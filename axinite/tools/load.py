import axinite as ax
from axinite.tools import AxiniteArgs
import json
from numba import jit
_jit = jit

def load(args: AxiniteArgs, path: str = "", dont_change_args: bool = False, jit: bool = True):
    if jit == False: args.action = lambda t, **kwargs: print(f"Timestep {t} ({((t / args.limit) * 100).value:.2f}% complete)", end="\r")

    bodies = ax.load(*args.unpack(), t=args.t, modifier=args.modifier, action=args.action)
    print(f"\nFinished with {len(bodies[0].r)} timesteps")

    if path == "": 
        if not dont_change_args:
            args.t = args.limit
            args.bodies = bodies
        return bodies
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

            for body in bodies: 
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
                args.bodies = bodies
            return bodies