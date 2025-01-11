import axinite.tools as axtools
import json

def save(args: axtools.AxiniteArgs, path: str):
    with open(path, 'w+') as f:
        data = {
            "name": args.name,
            "delta": args.delta.value,
            "limit": args.limit.value,
            "t": args.t.value,
            "radius_multiplier": args.radius_multiplier,
            "bodies": []
        }

        for body in args.bodies: 
            body_data = {
                "name": body.name,
                "mass": body.mass.value,
                "radius": body.radius.value,
                "r": {i: list(body.r(i)) for i in range(body._inner["r"].shape[0])},
                "v": {i: list(body.v(i)) for i in range(body._inner["v"].shape[0])}
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