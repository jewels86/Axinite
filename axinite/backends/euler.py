import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

@jit(nopython=False)
def euler(delta, limit, bodies, action=None, modifier=None, t=-1.0):
    if t == -1.0: t = 0.0 + delta
    timestep = 1
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j:
                    r = body["r"][timestep - 1] - other["r"][timestep - 1]
                    f += ax.gravitational_force_jit(body["m"], other["m"], r)
            a = f / body["m"]
            v = body["v"][timestep - 1] + a * delta
            r = body["r"][timestep - 1] + v * delta
            body["v"][timestep] = v
            body["r"][timestep] = r
        t += delta
        timestep += 1
        if action is not None: action(t, limit=limit, bodies=bodies, delta=delta)
    return bodies