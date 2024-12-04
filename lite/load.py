import axinite as ax
from lite import AxiniteArgs
import json

def load(args: AxiniteArgs, path: str):
    args.action = lambda t, **kwargs: print(f"Timestep {t} ({((t / args.limit) * 100).value:.2f}% complete)", end="\r")

    bodies = ax.load(*args.unpack(), t=args.t)

    if path == "": return bodies
    else: 
        with open(path, 'w+') as f:
            data = {
                "delta": args.delta.value,
                "limit": args.limit.value,
                "t": args.t.value,
                "bodies": []
            }

            for body in bodies: 
                data["bodies"].append({
                    "name": body.name,
                    "mass": body.mass.value,
                    "radius": body.radius.value,
                    "r": [[r.x.value, r.y.value, r.z.value] for r in body.r.values()],
                    "v": [[v.x.value, v.y.value, v.z.value] for v in body.v.values()]
                })

            json.dump(data, f, indent=4)
            return args.limit.value, bodies