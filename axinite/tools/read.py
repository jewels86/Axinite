import axinite as ax
from axinite.tools import AxiniteArgs, interpret_time, data_to_body
import astropy.units as u
import json

def read(path: str) -> AxiniteArgs:
    """Read a simulation from a file.

    Args:
        path (str): The path to read from.

    Returns:
        AxiniteArgs: The simulation result.
    """
    
    with open(path, 'r') as f:
        data = json.load(f)
        
        args = AxiniteArgs()
        args.name = data["name"]
        args.delta = interpret_time(data["delta"])
        args.limit = interpret_time(data["limit"])
        args.t = data["t"] * u.s

        if "radius_multiplier" in data:
            args.radius_multiplier = data["radius_multiplier"]

        if "rate" in data:
            args.rate = data["rate"]

        if "retain" in data:
            args.retain = data["retain"]

        if "frontend_args" in data:
            args.frontend_args = data["frontend_args"]

        for body in data["bodies"]: 
            args.bodies.append(data_to_body(body))

        return args