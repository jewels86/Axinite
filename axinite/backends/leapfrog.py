import numpy as np
from numba import njit, typed, types, jit
import axinite as ax

@jit(nopython=False)
def leapfrog(delta, limit, bodies, action=None, modifier=None, t=-1.0):
    @njit
    def a(_t, i):
        f = np.zeros(3)
        for j, other in enumerate(bodies):
            if i != j:
                r = bodies[i]["r"][_t] - other["r"][_t]
                f += ax.gravitational_force_jit(bodies[i]["m"], other["m"], r)
        return f / bodies[i]["m"]
    
    
