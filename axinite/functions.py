from astropy.coordinates import CartesianRepresentation
from astropy.units import Quantity
from astropy.constants import G
import astropy.units as u
import math
import numpy as np
import axinite as ax
from numba import njit

_G = G.value

def apply_to_vector(vector: CartesianRepresentation, function) -> CartesianRepresentation:
    """Applies a function to each component of a vector.

    Args:
        vector (CartesianRepresentation): The vector to apply the function to.
        function (_type_): The function to apply to the vector.

    Returns:
        CartesianRepresentation: The vector with the function applied to it.
    """
    return CartesianRepresentation([function(i) for i in vector.xyz])

def vector_to(vector: CartesianRepresentation, unit: Quantity) -> CartesianRepresentation:
    """Converts a vector to a specific unit.

    Args:
        vector (CartesianRepresentation): The vector to convert.
        unit (Quantity): The unit to convert the vector to.

    Returns:
        CartesianRepresentation: The vector in the new unit.
    """
    return apply_to_vector(vector, lambda i: i.to(unit))

def vector_magnitude(vector: CartesianRepresentation) -> float:
    """Calculates the magnitude of a vector.

    Args:
        vector (CartesianRepresentation): The vector to calculate the magnitude of.

    Returns:
        float: The magnitude of the vector.
    """
    return np.sqrt(vector.x**2 + vector.y**2 + vector.z**2)

def unit_vector(vector: CartesianRepresentation) -> CartesianRepresentation:
    """Calculates the unit vector of a vector.

    Args:
        vector (CartesianRepresentation): The vector to calculate the unit vector of.

    Returns:
        CartesianRepresentation: The unit vector of the vector.
    """
    return vector / vector_magnitude(vector)

def to_vector(data: dict, unit: u.Unit) -> CartesianRepresentation:
    """Converts a dictionary to a vector.

    Args:
        data (dict): The dictionary to convert.
        unit (u.Unit): The unit to convert the vector to.

    Returns:
        CartesianRepresentation: The vector.
    """
    return CartesianRepresentation(data["x"] * unit, data["y"] * unit, data["z"] * unit)

def to_body(body_dtype, delta):
    """Converts a body_dtype to an ax.Body object.

    Args:
        body_dtype (np.dtype): The body_dtype to convert.
        delta (u.Quantity): The change in time between each step.
        limit (u.Quantity): The limit of the simulation.

    Returns:
        ax.Body: The converted Body object.
    """
    mass = body_dtype["m"] * u.kg
    position = CartesianRepresentation(*body_dtype["r"][0], u.m)
    velocity = CartesianRepresentation(*body_dtype["v"][0], u.m/u.s)
    
    body = ax.Body(mass, position, velocity)
    body.name = body_dtype["n"]
    
    for i, r in enumerate(body_dtype["r"]):
        body.r[i * delta.value] = CartesianRepresentation(*r, u.m)
    for i, v in enumerate(body_dtype["v"]):
        body.v[i * delta.value] = CartesianRepresentation(*v, u.m/u.s)
    
    return body

def create_jit_bodies(bodies, limit, delta):
    body_dtype = np.dtype([
        ("n", "U20"),
        ("m", np.float64),
        ("r", np.float64, (int(limit.value/delta.value), 3)),
        ("v", np.float64, (int(limit.value/delta.value), 3))
    ])
    _bodies = np.zeros(len(bodies), dtype=body_dtype)
    for i, body in enumerate(bodies):
        _r = body.r.values()
        _v = body.v.values()
        r = np.zeros((int(limit.value/delta.value), 3))
        v = np.zeros((int(limit.value/delta.value), 3))
        for j, __r in enumerate(_r): 
            r[j][0] = __r.x.value
            r[j][1] = __r.y.value
            r[j][2] = __r.z.value
        for j, __v in enumerate(_v):
            v[j][0] = __v.x.value
            v[j][1] = __v.y.value
            v[j][2] = __v.z.value
        _bodies[i] = (body.name, body.mass.value, r, v)
    return _bodies

@njit 
def vector_magnitude_jit(vec: np.ndarray) -> float:
    """Calculates the magnitude of a vector.

    Args:
        vec (np.ndarray): The vector to calculate the magnitude of.

    Returns:
        float: The magnitude of the vector.
    """
    return np.sqrt(np.sum(vec**2))

@njit
def unit_vector_jit(vec: np.ndarray) -> np.ndarray:
    """Calculates the unit vector of a vector.

    Args:
        vec (np.ndarray): The vector to calculate the unit vector of.

    Returns:
        np.ndarray: The unit vector of the vector.
    """
    mag = vector_magnitude_jit(vec)
    return vec / mag if mag > 0 else vec

@njit
def gravitational_force_jit(m1: u.Quantity, m2: u.Quantity, r: np.ndarray) -> np.ndarray:
    """Calculates the gravitational force between two bodies.

    Args:
        m1 (u.Quantity): The mass of the first body.
        m2 (u.Quantity): The mass of the second body.
        r (np.ndarray): The vector between the two bodies.

    Returns:
        np.ndarray: The gravitational force between the two bodies.
    """
    mag = vector_magnitude_jit(r)
    if mag == 0:
        return np.zeros(3)
    return -_G *((m1 * m2) / mag**2) * unit_vector_jit(r)