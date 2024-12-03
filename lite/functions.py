import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation
import vpython as vp

def interpret_time(string: str):
    if string.endswith("min"):
        string = string.removesuffix("min")
        return float(string) * 60 * u.s 
    elif string.endswith("hr"): 
        string = string.removesuffix("hr")
        return float(string) * 3600 * u.s
    elif string.endswith("d"):
        string  = string.removesuffix("d")
        return float(string) * 86400 * u.s
    else: return float(string) * u.s

def array_to_vectors(array, unit):
    arr = []
    for a in array:
        arr.append(ax.to_vector(a, unit))
    return arr

def data_to_body(data):
    name = data["name"]
    mass = data["mass"] * u.kg
    
    if type(data["r"]) is dict:
        position = ax.to_vector(data["r"], u.m)
        velocity = ax.to_vector(data["v"], u.m/u.s)

        return ax.Body(name, mass, position, velocity, data["radius"] * u.m)
    else:
        position = [ax.to_vector(r, u.m) for r in data["r"]]
        velocity = [ax.to_vector(v, u.m/u.s) for v in data["v"]]

        body = ax.Body(name, mass, position[0], velocity[0], data["radius"] * u.m)

        for t, v in enumerate(position):
            body.r[t] = v
        for t, v in enumerate(velocity):
            body.v[t] = v
        
        return body

def to_vec(vector: CartesianRepresentation):
    return vp.vector(vector.x.value, vector.y.value, vector.z.value)