import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

@jit(nopython=False)
def verlet(delta, limit, bodies, action=None, modifier=None, t=-1.0):
    if t == -1.0: t = 0.0 + delta

    pseudo_previous = np.zeros((len(bodies), 3))
    for i, body in enumerate(bodies):
        pseudo_previous[i] = body["r"][0] - body["v"][0] * delta
    
    for i, body in enumerate(bodies):
        f = np.zeros(3)
        for j, other in enumerate(bodies):
            if i != j: f += ax.gravitational_force_jit(body["mass"], body["r"][t - delta] - other["r"][t - delta])
        a = f / body["mass"]
        body["r"][t] = 2 * body["r"][t - delta] - pseudo_previous[i] + a * delta**2

    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["mass"], other["mass"], body["r"][t] - other["r"][t])
            a = f / body["mass"]
            body["r"][t + delta] = 2 * body["r"][t] - body["r"][t - delta] + a * delta**2
        t += delta