import axinite as ax
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import CartesianRepresentation
from astropy.constants import G

m_earth = 5.972e24 * u.kg
r0_earth = CartesianRepresentation([0, 0, 0] * u.meter)
v0_earth = CartesianRepresentation([0, 0, 0] * u.meter / u.s)

m_moon = 7.342e22 * u.kg
r0_moon = CartesianRepresentation([3.844e8, 0, 0] * u.meter)
v0_moon = CartesianRepresentation([0, 1022, 0] * u.meter / u.s)

def g(r: CartesianRepresentation): 
    return -((G * m_earth) / r.magnitude**3) * r

r_moon = {
    0 * u.s: r0_moon,
}
v_moon = {
    0 * u.s: v0_moon,
}
a = {
    0 * u.s: CartesianRepresentation([0, 0, 0] * u.meter / u.s**2),
}
f = {
    0: g(r0_moon) * m_moon,
}

t = 0 * u.second
delta = (1 * u.hour).to(u.second)
limit = (30 * u.day).to(u.second)

while t < limit:
    