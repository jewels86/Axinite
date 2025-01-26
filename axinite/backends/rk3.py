import numpy as np
from numba import jit
import axinite as ax

def rk3_nojit_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    if t is None:
        t = 0.0
    n = 1
    rk_dtype = np.dtype([
        ("v_mid1", np.float64, (3,)),
        ("r_mid1", np.float64, (3,)),
        ("v_mid2", np.float64, (3,)),
        ("r_mid2", np.float64, (3,))
    ])

    while t < limit:
        _bodies = np.zeros(len(bodies), dtype=rk_dtype)
        for i, body in enumerate(bodies):
            f = ax.gravitational_forces(bodies, body, i, n-1)
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            a = f / body["m"]

            v_mid1 = body["v"][n-1] + (delta/2) * a
            r_mid1 = body["r"][n-1] + (delta/2) * v_mid1
            
            _bodies[i]["v_mid1"] = v_mid1
            _bodies[i]["r_mid1"] = r_mid1

        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], _bodies[j]["r_mid1"] - _bodies[i]["r_mid1"])
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            a = f / body["m"]

            v_mid2 = body["v"][n-1] + (delta/2) * a
            r_mid2 = body["r"][n-1] + (delta/2) * v_mid2
            
            _bodies[i]["v_mid2"] = v_mid2
            _bodies[i]["r_mid2"] = r_mid2

        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], _bodies[j]["r_mid2"] - _bodies[i]["r_mid2"])
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            a = f / body["m"]

            body["v"][n] = body["v"][n-1] + delta * a
            body["r"][n] = body["r"][n-1] + delta * body["v"][n]
        
        if action is not None and n % action_frequency == 0: action(bodies, t, limit=limit, delta=delta, n=n)
        n += 1
        t += delta
    
    return bodies

def rk3_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    compiled = jit(rk3_nojit_backend)
    return compiled(delta, limit, bodies, action, modifier, t, action_frequency)
