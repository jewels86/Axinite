import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

default_modifier = jit(lambda body, t, bodies, f: 0, nopython=False)
default_action = jit(lambda t, limit, delta, modifier, bodies: None, nopython=False)

@jit(nopython=False)
def _load_jit(delta, limit, bodies, action=default_action, modifier=default_modifier, t=-1.0):
    if t == -1.0: t = 0.0 + delta
    timestep = 1
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j:
                    r = body["r"][timestep - 1] - other["r"][timestep - 1]
                    f += ax.gravitational_force_jit(body["m"], other["m"], r)
            f += modifier(body, t, bodies=bodies, f=f)
            a = f / body["m"]
            v = body["v"][timestep - 1] + a * delta
            r = body["r"] [timestep - 1] + v * delta
            body["v"][timestep] = v
            body["r"][timestep] = r
        t += delta
        timestep += 1
        action(t, limit=limit, bodies=bodies, delta=delta)
    return bodies