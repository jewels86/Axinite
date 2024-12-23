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
def gravitational_force(mass1, mass2, r):
    return -G * ((mass1 * mass2) / vector_magnitude(r)**2) * unit_vector(r)

@njit
def load(delta, limit, action, bodies, t=0.0, modifiers=None):
    if modifiers is None: modifiers = typed.List.empty_list(types.ListType(types.float64[:]))
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j:
                    r_diff = body[""]