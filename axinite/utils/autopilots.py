import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

def rocket_autopilot(destination: np.ndarray, body: ax.Body, _bodies: np.ndarray, speed_max: np.float64, 
                     force_max: np.float64, turn_rate: np.float64, time: int) -> np.ndarray:
    n_body = -1
    for i, _body in enumerate(_bodies):
        if _body.name == body.name: n_body = i
    
    if n_body == -1: raise Exception("Couldn't find the body in bodies")

    @jit
    def fn(_body, f, bodies, t, delta, limit, n):
        if bodies[n_body]["n"] == _body["n"] and n < time:
            r_prev = _body["r"][n - 1]
            v_prev = _body["v"][n - 1]

            difference = destination - r_prev
            distance = ax.vector_magnitude_jit(difference)
            deceleration_dist = (speed_max ** 2) / (2 * force_max)
            distance_from_deceleration = distance - deceleration_dist
            unit_vector = ax.unit_vector_jit(difference)
            
            quaternion = axana.quaternion_between(unit_vector, v_prev)
            quaternion = axana.clip_quaternion_degrees(quaternion, turn_rate)
            target_unit_vector = axana.apply_quaternion(v_prev, quaternion)

            if distance_from_deceleration <= 0:
                force = target_unit_vector * -force_max
                force = np.clip(f, -force_max, force_max)
            else:
                force = target_unit_vector * force_max
            
            force = np.clip(f, -force_max, force_max)

            f = force + f

        return f
    return fn
