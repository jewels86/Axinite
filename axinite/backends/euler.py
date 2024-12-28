import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

def euler_nojit_backend(delta, limit, bodies, action=None, modifier=None, t=-1.0, action_frequency=200):
    if t == -1.0: t = 0.0 + delta
    n = 1
    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j:
                    r = body["r"][n - 1] - other["r"][n - 1]
                    f += ax.gravitational_force_jit(body["m"], other["m"], r)
            if modifier is not None: f = modifier(body, f)
            a = f / body["m"]
            v = body["v"][n - 1] + a * delta
            r = body["r"][n - 1] + v * delta
            body["v"][n] = v
            body["r"][n] = r
        t += delta
        n += 1
        if action is not None and n % action_frequency == 0: action(bodies, t)
    return bodies

@jit(nopython=False)
def euler_backend(delta, limit, bodies, action=None, modifier=None, t=-1.0, action_frequency=200):
    return jit(euler_nojit_backend, nopython=True)(delta, limit, bodies, action=action, modifier=modifier, t=t, action_frequency=action_frequency)