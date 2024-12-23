import numpy as np
from numba import njit, typed, types

G = 6.67430e-11

@njit 
def vector_magnitude(vec):
    return np.sqrt(np.sum(vec**2))

@njit
def unit_vector(vec):
    mag = vector_magnitude(vec)
    return vec / mag if mag > 0 else vec

@njit
def gravitational_force(m1, m2, r):
    mag = vector_magnitude(r)
    if mag == 0:
        return np.zeros(3)
    return -G *((m1 * m2) / mag**2) * unit_vector(r)

@njit
def _load_jit(delta, limit, bodies):
    