import math
import numpy as np
import axinite as ax
from numba import njit

G = 6.67430e-11
def body_dtype(limit, delta):
    """
    Returns the data type for a body.

    Args:
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        np.dtype: The data type for a body.
    """
    return np.dtype([
    ("n", "U20"),
    ("m", np.float64),
    ("r", np.float64, (int(limit/delta), 3)),
    ("v", np.float64, (int(limit/delta), 3))
])
def _body(limit, delta, name, mass): 
    """
    Creates a new body.

    Args:
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.
        name (str): The name of the body.
        mass (np.float64): The mass of the body in kilograms.

    Returns:
        np.ndarray: The new body.
    """
    return np.array((name, mass, np.zeros((int(limit/delta), 3)), np.zeros((int(limit/delta), 3))), dtype=ax.body_dtype(limit, delta))

def get_inner_bodies(bodies):
    """
    Returns the inner representation of a list of bodies.

    Args:
        bodies (list[ax.Body]): A list of Body objects.

    Returns:
        tuple: The inner representation of the bodies.
    """
    _bodies = ()
    for body in bodies: _bodies += (body._inner,)
    return _bodies

def create_outer_bodies(bodies, limit, delta):
    """
    Creates outer body representations from inner bodies.

    Args:
        bodies (np.ndarray): An array of inner body representations.
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        list[ax.Body]: A list of Body objects.
    """
    _bodies = []
    for body in bodies:
        _body = ax.Body(str(body["n"]), body["m"], limit, delta)
        _body._inner = body
        _bodies.append(_body)
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
def gravitational_force_jit(m1: np.float64, m2: np.float64, r: np.ndarray) -> np.ndarray:
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
    return -G *((m1 * m2) / mag**2) * unit_vector_jit(r)