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
def _load_jit(delta, limit, bodies, action=None):
    t = 0.0 + delta
    timestep = 1
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j:
                    r = body["r"][timestep - 1] - other["r"][timestep - 1]
                    f += gravitational_force(body["m"], other["m"], r)
            a = f / body["m"]
            v = body["v"][timestep - 1] + a * delta
            r = body["r"] [timestep - 1] + v * delta
            body["v"][timestep] = v
            body["r"][timestep] = r
        t += delta
        timestep += 1
        if action is not None: action(t, limit=limit, bodies=bodies, delta=delta)
    return bodies