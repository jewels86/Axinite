import matplotlib.pyplot as plt
import numpy as np
import axinite as ax
from astropy import units as u
from astropy.coordinates import CartesianRepresentation
import math
import sympy as sp

P = 1.21 * u.kilogram / u.meter**3
m = 75 * u.kilogram
A = 0.18 * u.meter**2
C = 0.7
v_initial = 0 * u.meter / u.second
r_initial = CartesianRepresentation(0 * u.meter, 18000 * u.meter, 0 * u.meter)
theta = -90
g = CartesianRepresentation([0, -9.81, 0] * u.meter / u.second**2)

r0 = r_initial
v0 = CartesianRepresentation(math.cos(theta) * v_initial, math.sin(theta) * v_initial, 0 * u.meter / u.second)

F_grav = m * g

f = {}
a = {}
v = {
    0 * u.second: v0
}
r = {
    0 * u.second: r0
}

delta_t = 0.5 * u.second

t = 0 * u.second + delta_t

while r[t - delta_t].y > 0:
    f[t] = F_grav + (0.5 * P * A * C * (ax.apply_to_vector(v[t - delta_t], lambda x: x**2)))
    a[t] = f[t] / m
    v[t] = (delta_t * a[t]) + v[t - delta_t]
    r[t] = (delta_t * v[t]) + r[t - delta_t]
    print("Timestep: ", t, end="\r")
    t += delta_t
    print(r)