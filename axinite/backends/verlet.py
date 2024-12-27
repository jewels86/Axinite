import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

@jit(nopython=False)
def verlet(delta, limit, bodies, action=None, modifier=None, t=0.0):
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["mass"], other["mass"], body["r"][t] - other["r"][t])
            a = f / body["mass"]
            body["r"][t + delta] = 2 * body["r"][t] - body["r"][t - delta] + a * delta**2
            