import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation
from typing import Literal
import vpython as vp
import numpy as np
import axinite.tools as axtools

def interpret_time(string: str) -> u.Quantity:
    """Interprets a string as a time in seconds.

    Args:
        string (str): The string to interpret.

    Returns:
        u.Quantity: The time in seconds.
    """
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

def array_to_vectors(array: list[dict[str, np.float64]], unit: u.Unit) -> list[CartesianRepresentation]:
    """Converts a list of dicts to a list of vectors.

    Args:
        array (list[dict[str, np.float64]]): A list of dicts to convert.
        unit (u.Unit): The unit to convert to.

    Returns:
        list[CartesianRepresentation]: The list of vectors.
    """
    arr = []
    for a in array:
        arr.append(ax.to_vector(a, unit))
    return arr

def data_to_body(data: dict[str, any]) -> axtools.Body:
    """Converts a dict to a Body object.

    Args:
        data (dict[str, any]): The dict to convert.

    Returns:
        axtools.Body: The Body object.
    """

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

def vector_from_list(vector: list[np.float64], unit: u.Unit) -> CartesianRepresentation:
    """Converts a list to a vector.

    Args:
        vector (list[np.float64]): The list to convert
        unit (u.Unit): The unit to convert to.

    Returns:
        CartesianRepresentation: The vector.
    """

    return CartesianRepresentation(u.Quantity(float(vector[0]), unit), u.Quantity(float(vector[1]), unit), u.Quantity(float(vector[2]), unit))

def to_float(val: any) -> np.float64:
    """Legacy shorthand for converting to np.float64.

    Args:
        val (any): The value to convert.

    Returns:
        np.float64: The result.
    """

    return np.float64(val)

def string_to_color(color_name: str, frontend: Literal['vpython', 'mpl', 'plotly']) -> vp.color | str:
    """Converts a string to a color object for a given frontend.

    Args:
        color_name (str): The name of the color.
        frontend (str): The frontend to convert for.

    Returns:
        vp.color | str: The converted color.
    """
    if frontend == "vpython":
        color_map = {
            'red': vp.color.red,
            'blue': vp.color.blue,
            'green': vp.color.green,
            'orange': vp.color.orange,
            'purple': vp.color.purple,
            'yellow': vp.color.yellow,
            'white': vp.color.white,
            'gray': vp.color.gray(0.5)
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
            'white': 'white',
            'gray': 'gray'
        }
        return color_map.get(color_name, 'white')
    
def create_sphere(pos: CartesianRepresentation, radius: u.Quantity, n=20) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generates the vertices of a sphere.

    Args:
        pos (CartesianRepresentation): The position of the sphere.
        radius (u.Quantity): The radius of the sphere.
        n (int, optional): Number of segments used to generate verticies. Defaults to 20.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: The x, y, and z coordinates of the sphere.
    """
    u1 = np.linspace(0, 2 * np.pi, n)
    v1 = u1.copy()
    uu, vv = np.meshgrid(u1, v1)

    xx = pos.x.value + radius.value * np.cos(uu) * np.sin(vv)
    yy = pos.y.value + radius.value * np.sin(uu) * np.sin(vv)
    zz = pos.z.value + radius.value * np.cos(vv)

    return xx, yy, zz

def max_axis_length(*bodies: axtools.Body, radius_multiplier: int = 1) -> np.float64:
    """Finds the maximum axis length of a set of bodies.

    Args:
        radius_multiplier (int, optional): The radius multiplier to apply. Defaults to 1.

    Returns:
        np.float64: The longest axis length found.
    """

    max_length = 0
    for body in bodies:
        x_length = max([v.x.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        y_length = max([v.y.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        z_length = max([v.z.value for k, v in body.r.items()]) + body.radius.value * radius_multiplier
        
        max_length = max(max_length, x_length, y_length, z_length)
    
    return max_length

def min_axis_length(*bodies: axtools.Body, radius_multiplier: int = 1) -> np.float64:
    """Finds the minimum axis length of a set of bodies.

    Args:
        radius_multiplier (int, optional): The radius multiplier to apply. Defaults to 1.

    Returns:
        np.float64: The lowest axis length found.
    """
    
    min_length = 0
    for body in bodies:
        x_length = min([v.x.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        y_length = min([v.y.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        z_length = min([v.z.value for k, v in body.r.items()]) - body.radius.value * radius_multiplier
        
        min_length = min(min_length, x_length, y_length, z_length)
    
    return min_length