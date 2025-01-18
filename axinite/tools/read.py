import axinite as ax
import axinite.tools as axtools
import json

def read(path: str) -> axtools.AxiniteArgs:
    """Read a simulation from a file.

    Args:
        path (str): The path to read from.

    Returns:
        AxiniteArgs: The simulation result.
    """
    
    with open(path, 'r') as f:
        data = json.load(f)
        
        args = axtools.AxiniteArgs()
        args.name = data["name"]
        args.delta = ax.interpret_time(data["delta"])
        args.limit = ax.round_limit(ax.interpret_time(data["limit"]), args.delta)
        args.t = data["t"]

        if "radius_multiplier" in data:
            args.radius_multiplier = data["radius_multiplier"]

        if "rate" in data:
            args.rate = data["rate"]

        if "retain" in data:
            args.retain = data["retain"]

        if "frontend_args" in data:
            args.frontend_args = data["frontend_args"]

        for body in data["bodies"]: 
            args.bodies.append(axtools.data_to_body(body, args.limit, args.delta))

        return args