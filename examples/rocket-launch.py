import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana
from numba import njit
import numpy as np

ACCELERATION_RATE = 25
THRUST_MAX = 7.36e5
TURN_RATE = 3

args = axtools.read("examples/rocket-launch.tmpl.ax")
bodies = axtools.load(args, verbose=True)

result = axana.intercept(bodies[3], bodies[2], (0, 1.1e4), ax.timesteps(args.limit, args.delta), args.delta, True)

print(f"Speed: {result[0]} m/s")
print(f"Position: {result[1]} m")
print(f"Time: {result[2]} n")
print(f"Unit Vector: {result[3]}")

speed = result[0]
position = result[1]
time = result[2]
unit_vector = result[3]

@njit
def modifier(body, f, bodies, t, delta, limit, n):
    if bodies[2]["n"] == body["n"] and time - n > 0:
        r_prev = body["r"][n - 1]
        v_prev = body["v"][n - 1]
        print(ax.vector_magnitude_jit(v_prev))

        difference = position - r_prev
        distance = ax.vector_magnitude_jit(difference)
        timesteps_left = time - n
        avg_speed = distance / (timesteps_left * delta)
        target = avg_speed - ax.vector_magnitude_jit(v_prev)
        acceleration = target / delta
        acceleration = ax.clip_scalar(acceleration, -ACCELERATION_RATE * delta, ACCELERATION_RATE * delta)

        quaternion = axana.quaternion_between(v_prev, unit_vector)
        quaternion = axana.clip_quaternion_degrees(quaternion, TURN_RATE)
        
        if ax.vector_magnitude_jit(v_prev) == 0: v_prev = unit_vector
        v = axana.apply_quaternion(v_prev, quaternion)
        _acceleration = ax.unit_vector_jit(v) * acceleration

        f = axana.apply_quaternion(_acceleration, quaternion) * body["m"]
        f = np.clip(f, -THRUST_MAX, THRUST_MAX)
        return f

    if bodies[2]["n"] == body["n"] and time - n == 0:
        v_prev = body["v"][n - 1]
        print(ax.vector_magnitude_jit(v_prev))
        a = -v_prev / delta
        f = a * body["m"]
        return f

    if bodies[2]["n"] == body["n"] and time - n < 0:
        f = np.zeros(3)
        return f
        
    return f

args2 = axtools.read("examples/rocket-launch.tmpl.ax")
args2.modifier = modifier
axtools.load(args2, "rocket-launch.ax", verbose=True)