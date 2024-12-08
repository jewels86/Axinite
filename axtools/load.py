import axinite as ax
from axtools import AxiniteArgs
import json

def load(args: AxiniteArgs, path: str):
    args.action = lambda t, **kwargs: print(f"Timestep {t} ({((t / args.limit) * 100).value:.2f}% complete)", end="\r")

    bodies = ax.load(*args.unpack(), t=args.t)
    print(f"\nFinished with {len(bodies[0].r)} timesteps")

    if path == "": return bodies
    else: 
        with open(path, 'w+') as f:
            data = {
                "delta": args.delta.value,
                "limit": args.limit.value,
                "t": args.t.value,
                "radius_multiplier": args.radius_multiplier,
                "bodies": []
            }

            for body in bodies: 
                data["bodies"].append({
                    "name": body.name,
                    "mass": body.mass.value,
                    "radius": body.radius.value,
                    "r": {k: [v.x.value, v.y.value, v.z.value] for k, v in body.r.items()},
                    "v": {k: [v.x.value, v.y.value, v.z.value] for k, v in body.v.items()}
                })

            if args.radius_multiplier is not None:
                data["radius_multiplier"] = args.radius_multiplier

            if args.rate is not None:
                data["rate"] = args.rate

            if args.retain is not None:
                data["retain"] = args.retain

            json.dump(data, f, indent=4)
            return args.limit.value, bodies