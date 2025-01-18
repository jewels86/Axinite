import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana
import axinite.utils as axutils
from numba import njit
import numpy as np

# This is VERY unfinished. It will not work.

ACCELERATION_RATE = 25
THRUST_MAX = 7.36e5
TURN_RATE = 3

args = axtools.read("examples/rocket-mission/rocket-mission.tmpl.ax")
bodies = axtools.load(args, verbose=True)

result = axana.intercept(
    bodies[3], bodies[2], (0, 1.1e4), ax.timesteps(args.limit, args.delta), args.delta, verbose=True
)

print(f"Speed: {result[0]} m/s")
print(f"Position: {result[1]} m")
print(f"Time: {result[2]} n")
print(f"Unit Vector: {result[3]}")

speed = result[0]
position = result[1]
time = result[2]
unit_vector = result[3]

args2 = axtools.read("examples/rocket-launch.tmpl.ax")
args2.modifier = axutils.rocket_autopilot(
    position, bodies[2], bodies, 1.1e4, THRUST_MAX, TURN_RATE, time
)
axtools.load(args2, "rocket-launch.ax", verbose=True)