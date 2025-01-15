import axinite as ax
from typing import Literal
import vpython as vp
import numpy as np
import axinite.tools as axtools
from numba import njit

def data_to_body(data: dict[str, any], limit, delta) -> axtools.Body:
    """Converts a dict to a Body object.

    Args:
        data (dict[str, any]): The dict to convert.

    Returns:
        axtools.Body: The Body object.
    """

    name = data["name"]
    mass = ax.interpret_mass(data["mass"])

    position = np.array([
        ax.interpret_distance(data["r"][0][0]),
        ax.interpret_distance(data["r"][0][1]),
        ax.interpret_distance(data["r"][0][2])  
    ])
    velocity = np.array([
        ax.interpret_distance(data["v"][0][0]),
        ax.interpret_distance(data["v"][0][1]),
        ax.interpret_distance(data["v"][0][2])
    ])
    body = axtools.Body(name, mass, limit, delta, position, velocity)
    body.radius = ax.interpret_distance(data["radius"])

    if "color" in data:
        body.color = data["color"]
    if "light" in data:
        body.light = data["light"]
    if "retain" in data:
        body.retain = data["retain"]

    for i in range(len(data["r"])):
        body._inner["r"][i] = np.array([
            ax.interpret_distance(data["r"][i][0]),
            ax.interpret_distance(data["r"][i][1]),
            ax.interpret_distance(data["r"][i][2])
        ])
    for i in range(len(data["v"])):
        body._inner["v"][i] = np.array([
            ax.interpret_distance(data["v"][i][0]),
            ax.interpret_distance(data["v"][i][1]),
            ax.interpret_distance(data["v"][i][2])
        ])

    return body

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

def create_sphere(pos: np.ndarray, radius: np.float64, n=20) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generates the vertices of a sphere.

    Args:
        pos (np.ndarray): The position of the sphere.
        radius (np.float64): The radius of the sphere.
        n (int, optional): Number of segments used to generate verticies. Defaults to 20.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: The x, y, and z coordinates of the sphere.
    """
    u1 = np.linspace(0, 2 * np.pi, n)
    v1 = u1.copy()
    uu, vv = np.meshgrid(u1, v1)

    xx = pos[0] + radius * np.cos(uu) * np.sin(vv)
    yy = pos[0] + radius * np.sin(uu) * np.sin(vv)
    zz = pos[0] + radius * np.cos(vv)

    return xx, yy, zz

def sphere_has(point: np.ndarray, sphere_pos: np.ndarray, radius: np.float64) -> bool:
    """Checks if a point is inside a sphere.

    Args:
        point (np.ndarray): The point to check.
        sphere_pos (np.ndarray): The position of the sphere.
        radius (np.float64): The radius of the sphere.

    Returns:
        bool: True if the point is inside the sphere, False otherwise.
    """
    distance = np.linalg.norm(point - sphere_pos)
    return distance <= radius

def max_axis_length(*bodies: axtools.Body, radius_multiplier: int = 1) -> np.float64:
    """Finds the maximum axis length of a set of bodies.

    Args:
        radius_multiplier (int, optional): The radius multiplier to apply. Defaults to 1.

    Returns:
        np.float64: The longest axis length found.
    """

    max_length = 0
    for body in bodies:
        x_length = max([v[0] for v in body._inner["r"]]) + body.radius * radius_multiplier
        y_length = max([v[1] for v in body._inner["r"]]) + body.radius * radius_multiplier
        z_length = max([v[2] for v in body._inner["r"]]) + body.radius * radius_multiplier
        
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
        x_length = min([v[0] for v in body._inner["r"]]) - body.radius * radius_multiplier
        y_length = min([v[1] for v in body._inner["r"]]) - body.radius * radius_multiplier
        z_length = min([v[2] for v in body._inner["r"]]) - body.radius * radius_multiplier
        
        min_length = min(min_length, x_length, y_length, z_length)
    
    return min_length

def from_body(body: ax.Body) -> axtools.Body:
    """Converts an ax.Body object to an axtools.Body object.

    Args:
        body (ax.Body): The Body object to convert.

    Returns:
        axtools.Body: The converted Body object.
    """

    _body = axtools.Body(body.name, body.mass, body.limit, body.delta, body._inner["r"][0], body._inner["v"][0])

    for i, r in enumerate(body._inner["r"]):
        _body._inner["r"][i] = r
    for i, v in enumerate(body._inner["v"]):
        _body._inner["v"][i] = v

    return _body