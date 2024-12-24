from astropy.coordinates import CartesianRepresentation
from astropy.units import Quantity
from astropy.constants import G
import astropy.units as u
import math
import numpy as np
from numba import njit

_G = G.value

def apply_to_vector(vector: CartesianRepresentation, function):
    return CartesianRepresentation([function(i) for i in vector.xyz])

def vector_to(vector: CartesianRepresentation, unit: Quantity):
    return apply_to_vector(vector, lambda i: i.to(unit))

def vector_magnitude(vector: CartesianRepresentation):
    return np.sqrt(vector.x**2 + vector.y**2 + vector.z**2)

def unit_vector(vector: CartesianRepresentation):
    return vector / vector_magnitude(vector)

def to_vector(data, unit):
    return CartesianRepresentation(data["x"] * unit, data["y"] * unit, data["z"] * unit)

@njit 
def vector_magnitude_jit(vec):
    return np.sqrt(np.sum(vec**2))

@njit
def unit_vector_jit(vec):
    mag = vector_magnitude_jit(vec)
    return vec / mag if mag > 0 else vec

@njit
def gravitational_force_jit(m1, m2, r):
    mag = vector_magnitude_jit(r)
    if mag == 0:
        return np.zeros(3)
    return -_G *((m1 * m2) / mag**2) * unit_vector_jit(r)