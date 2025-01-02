from astropy.coordinates import CartesianRepresentation
from astropy.units import Quantity
from astropy.constants import G
import astropy.units as u
import math
import numpy as np
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