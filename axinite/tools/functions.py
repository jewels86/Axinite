import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation
import vpython as vp
import numpy as np
import axinite.tools as axtools

def interpret_time(string: str):
    if type(string) is float: return string * u.s
    if string.endswith("min"):
        string = string.removesuffix("min")
        return float(string) * 60 * u.s 
    elif string.endswith("hr"): 
        string = string.removesuffix("hr")
        return float(string) * 3600 * u.s
    elif string.endswith("d"):
        string  = string.removesuffix("d")
        return float(string) * 86400 * u.s
    elif string.endswith("yr"):
        string = string.removesuffix("yr")
        return float(string) * 31536000 * u.s
    else: return float(string) * u.s

def array_to_vectors(array, unit):
    arr = []
    for a in array:
        arr.append(ax.to_vector(a, unit))
    return arr

def data_to_body(data):
    name = data["name"]
    mass = data["mass"] * u.kg
    
    if "x" in data["r"]:
        position = ax.to_vector(data["r"], u.m)
        velocity = ax.to_vector(data["v"], u.m/u.s)

        body = axtools.Body(name, mass, position, velocity, data["radius"] * u.m)

        if "color" in data:
            body.color = data["color"]
        if "light" in data:
            body.light = data["light"]
        if "retain" in data:
            body.retain = data["retain"]

        return body
    else:
        position = [vector_from_list(r, u.m) for r in data["r"].values()]
        velocity = [vector_from_list(v, u.m/u.s) for v in data["v"].values()]

        body = axtools.Body(name, mass, position[0], velocity[0], data["radius"] * u.m)

        for t, r in data["r"].items():
            body.r[to_float(t)] = vector_from_list(r, u.m)
        for t, v in data["v"].items():
            body.v[to_float(t)] = vector_from_list(v, u.m)

        if "color" in data:
            body.color = data["color"]
        if "light" in data:
            body.light = data["light"]
        if "retain" in data:
            body.retain = data["retain"]
        if "radius_multiplier" in data:
            body.radius *= data["radius_multiplier"]
        
        return body

def vector_from_list(vector: list, unit):
    return CartesianRepresentation(u.Quantity(float(vector[0]), unit), u.Quantity(float(vector[1]), unit), u.Quantity(float(vector[2]), unit))

def to_float(val):
    return np.float64(val)

def string_to_color(color_name, frontend: str):
    if frontend == "vpython":
        color_map = {
            'red': vp.color.red,
            'blue': vp.color.blue,
            'green': vp.color.green,
            'orange': vp.color.orange,
            'purple': vp.color.purple,
            'yellow': vp.color.yellow,
            'white': vp.color.white
        }
        return color_map.get(color_name, vp.color.white)
    elif frontend == "matplotlib":
        color_map = {
            'red': 'r',
            'blue': 'b',
            'green': 'g',
            'orange': 'orange',
            'purple': 'purple',
            'yellow': 'yellow',
            'white': 'white'
        }
        return color_map.get(color_name, 'white')
    

def create_sphere(pos: CartesianRepresentation, radius: u.Quantity, n=20):
    u1 = np.linspace(0, 2 * np.pi, n)
    v1 = u1.copy()
    uu, vv = np.meshgrid(u1, v1)

    xx = pos.x.value + radius.value * np.cos(uu) * np.sin(vv)
    yy = pos.y.value + radius.value * np.sin(uu) * np.sin(vv)
    zz = pos.z.value + radius.value * np.cos(vv)

    return xx, yy, zz

def max_axis_length(*bodies, radius_multiplier=1):
    max_length = 0
    for body in bodies:
        x_length = max([v.x.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        y_length = max([v.y.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        z_length = max([v.z.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        
        max_length = max(max_length, x_length, y_length, z_length)
    
    return max_length

def min_axis_length(*bodies, radius_multiplier=1):
    min_length = 0
    for body in bodies:
        x_length = min([v.x.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        y_length = min([v.y.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        z_length = min([v.z.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        
        min_length = min(min_length, x_length, y_length, z_length)
    
    return min_length