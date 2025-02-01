import axinite.tools as axtools
import json

def save(args: axtools.AxiniteArgs, path: str):
    """
    Saves the simulation data to a file.

    Args:
        args (axtools.AxiniteArgs): The arguments for the simulation.
        path (str): The path to save the simulation data to.
    """

    with open(path, "w") as file:
        file.write(saves(args))

def saves(args: axtools.AxiniteArgs):
    """
    Converts the simulation data to a JSON string.

    Args:
        args (axtools.AxiniteArgs): The arguments for the simulation.

    Returns:
        str: The JSON string representation of the simulation data.
    """

    data = {
        "name": args.name,
        "delta": float(args.delta),
        "limit": float(args.limit),
        "t": float(args.t),
        "bodies": []
    }

    for body in args.bodies: 
        body_data = {
            "name": str(body.name),
            "mass": float(body.mass),
            "radius": float(body.radius),
            "r": [],
            "v": []
        }

        for i, r in enumerate(body._inner["r"]):
            v = body._inner["v"][i]
            _r = [float(_v) for _v in r]
            body_data["r"].append(_r)
            _v = [float(__v) for __v in v]
            body_data["v"].append(_v)

        if body.color != None:
            body_data["color"] = body.color
        if body.retain != None:
            body_data["retain"] = int(body.retain)
        if body.light != None:
            body_data["light"] = body.light

        data["bodies"].append(body_data)

    if args.radius_multiplier is not None:
        data["radius_multiplier"] = int(args.radius_multiplier)

    if args.rate is not None:
        data["rate"] = args.rate

    if args.retain is not None:
        data["retain"] = args.retain
    
    if args.frontend_args != {}:
        data["frontend_args"] = args.frontend_args

    return json.dumps(data)