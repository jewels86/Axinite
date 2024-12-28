import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

@jit(nopython=False)
def verlet_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    if t != 0.0: raise Exception("Verlet method does not support non-zero initial time.")
    t = 0.0 + delta 
    n = 1

    for i, body in enumerate(bodies):
        f = np.zeros(3)
        for j, other in enumerate(bodies):
            if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][0] - other["r"][0])
        body["r"][1] = body["r"][0] + body["v"][0] * delta + 0.5 * (f / body["m"]) * delta**2
        body["v"][1] = (body["r"][1] - body["r"][0]) / (2 * delta)
    
    n += 1
    t += delta

    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][n-1] - other["r"][n-1])
            if modifier is not None: f = modifier(body, f)

            body["r"][n] = body["r"][n-1] * 2 - body["r"][n-2] + (f / body["m"]) * delta**2
            body["v"][n] = (body["r"][n] - body["r"][n-1]) / (2 * delta)
        if action is not None and n % action_frequency == 0: action(bodies, t)
        n += 1
        t += delta
    
    return bodies

def verlet_nojit_backend(delta, limit, bodies, action=None, modifier=None, t=0.0):
    if t != 0.0: raise Exception("Verlet method does not support non-zero initial time.")
    t = 0.0 + delta 
    n = 1

    for i, body in enumerate(bodies):
        f = np.zeros(3)
        for j, other in enumerate(bodies):
            if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][0] - other["r"][0])
        body["r"][1] = body["r"][0] + body["v"][0] * delta + 0.5 * (f / body["m"]) * delta**2
        body["v"][1] = (body["r"][1] - body["r"][0]) / (2 * delta)
    
    n += 1
    t += delta

    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][n-1] - other["r"][n-1])

            body["r"][n] = body["r"][n-1] * 2 - body["r"][n-2] + (f / body["m"]) * delta**2
            body["v"][n] = (body["r"][n] - body["r"][n-1]) / (2 * delta)

        n += 1
        t += delta
    
    return bodies