import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana
from numba import njit
import numpy as np

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
    if bodies[2]["n"] == body["n"]:
        if n != 1:
            return np.array([0.0, 0.0, 0.0])
        
        v = speed * unit_vector
        a = v / delta
        return body["m"] * a
    return f

args2 = axtools.read("examples/rocket-launch.tmpl.ax")
args2.modifier = modifier
axtools.load(args2, "rocket-launch.ax", verbose=True)