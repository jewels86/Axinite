import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

def rocket_autopilot(self, destination: np.ndarray, body: ax.Body,
                     bodies: np.ndarray, speed_max: np.float64, 
                     force_max: np.float64, turn_rate: np.float64, 
                     acceleration_rate: np.float64, delta: np.float64, 
                     time: int) -> np.ndarray:
    n_body = -1
    for i, _body in enumerate(bodies):
        if _body.name == body.name: n_body = i
    
    if n_body == -1: raise Exception("Couldn't find the body in bodies")

    @jit
    def fn(_body, f, _bodies, t, delta, limit, n):
        if _bodies[n_body] == body:
            r_prev = _body["r"][n - 1]
            v_prev = _body["v"][n - 1]

            difference = destination - r_prev
            distance = ax.vector_magnitude_jit(difference)
            unit_vector = ax.unit_vector_jit(difference)
            speed = ax.vector_magnitude_jit(v_prev)
            time_left = deacceleration_time - n

            target = distance / time_left
            target = target - speed
            target = ax.clip_scalar(target, -speed_max, speed_max)

            quaternion = axana.quaternion_between(unit_vector, v_prev)
            quaternion = axana.clip_quaternion_degrees(quaternion, turn_rate * delta)
            target = axana.apply_quaternion(ax.unit_vector_jit(v_prev), quaternion)
            acceleration = target - v_prev / delta
            acceleration = ax.clip_scalar(acceleration, -acceleration_rate * delta, acceleration_rate * delta)
            force = acceleration * _body["mass"]
            force = ax.clip_scalar(force, -force_max, force_max)

            deacceleration_time = speed / acceleration_rate
            f = force + f

        return f
    
    return fn