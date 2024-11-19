from astropy.coordinates import CartesianRepresentation
import astropy.units as u
import axinite as ax
import numpy as np
import math

sun = ax.Body(
    1.989e30 * u.kg,
    CartesianRepresentation([0, 0, 0] * u.m),
    CartesianRepresentation([0, 0, 0] * u.m/u.s)
)
earth = ax.Body(
    5.972e24 * u.kg,
    CartesianRepresentation([1.471e11, 0, 0] * u.m),
    CartesianRepresentation([0, 0, 3.03e4] * u.m/u.s)
)
moon = ax.Body(
    7.342e22 * u.kg,
    CartesianRepresentation([3.844e8 + earth.r0.x.value, 0, 0] * u.m),
    CartesianRepresentation([0, 1.095e3, 1.095e3] * u.m/u.s)
)

section_length = 60 * u.day
section_count = 0
t = 0 * u.s
section_t = 0 * u.s
delta = 1 * u.hour
limit = 360 * u.day

while t < limit:
    for i in range()