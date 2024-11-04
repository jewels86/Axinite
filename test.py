import axinite as ax
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import CartesianRepresentation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

A = ax.Body(
    "A", 
    1 * u.kg,
    CartesianRepresentation([1, 1, 1] * u.kilometer),
    CartesianRepresentation([0.1, 0, 0] * u.kilometer / u.second),
    0.1 * u.kilometer
)
B = ax.Body(
    "B",
    1 * u.kg,
    CartesianRepresentation([-1, -1, -1] * u.kilometer),
    CartesianRepresentation([-0.1, 0, 0] * u.kilometer / u.second),
    0.1 * u.kilometer
)

t = 0
delta_t = 1200 * u.second
dt_val = delta_t.value
length = delta_t / 3600

rB = {
    0: B.position
}
vB = {
    0: B.velocity
}
aB = {
    0: A.gravitational_force(B)
}

print("Computing simulation...")

try:
    for i in range(0, round(length.value)):
        aB[t + dt_val] = A.gravitational_force(B)
        vB[t + dt_val] = vB[t] + (aB[t + dt_val] * delta_t)
        rB[t + dt_val] = rB[t] + (vB[t + dt_val] * delta_t)

        t += dt_val
        print(f"Timestep: {t} ({round(i / 3.6)}% - {i})", end="\r")
except KeyboardInterrupt as e:
    pass

print(f"\nReady with {t / dt_val} frames.")

