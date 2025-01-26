import numpy as np
from numba import jit
import axinite as ax

def rk2_nojit_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    if t == None:
        t = 0.0
    n = 1
    rk_dtype = np.dtype([
        ("v_mid", np.float64, (3,)),
        ("r_mid", np.float64, (3,))
    ])

    while t < limit:
        _bodies = np.zeros(len(bodies), dtype=rk_dtype)
        for i, body in enumerate(bodies):
            f = ax.gravitational_forces(bodies, body, i, n-1)
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            a = f / body["m"]

            v_mid = body["v"][n-1] + (delta/2) * a
            r_mid = body["r"][n-1] + (delta/2) * v_mid
            
            _bodies[i]["v_mid"] = v_mid
            _bodies[i]["r_mid"] = r_mid
        
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], _bodies[j]["r_mid"] - _bodies[i]["r_mid"])
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            a = f / body["m"]
            body["v"][n] = _bodies[i]["v_mid"] + delta * a
            body["r"][n] = _bodies[i]["r_mid"] + delta * body["v"][n]
        
        if action is not None and n % action_frequency == 0: action(bodies, t, limit=limit, delta=delta, n=n)
        n += 1
        t += delta
    
    return bodies

def rk2_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    compiled = jit(rk2_nojit_backend)
    return compiled(delta, limit, bodies, action, modifier, t, action_frequency)