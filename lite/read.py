import axinite as ax
from lite import AxiniteArgs, interpret_time, data_to_body
import astropy.units as u
import json

def read(path: str) -> AxiniteArgs:
    with open(path, 'r') as f:
        data = json.load(f)
        
        args = AxiniteArgs()
        args.delta = interpret_time(data["delta"])
        args.limit = interpret_time(data["limit"])
        args.t = data["t"] * u.s

        if "radius_multiplier" in data:
            args.radius_multiplier = data["radius_multiplier"]

        for body in data["bodies"]: 
            args.bodies.append(data_to_body(body))

        return args