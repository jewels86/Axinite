import axinite as ax
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from scipy import signal
import json

m_earth = 5.972e24 * u.kg
r0_earth = CartesianRepresentation([0, 0, 0] * u.meter)
v0_earth = CartesianRepresentation([0, 0, 0] * u.meter / u.s)

m_moon = 7.342e22 * u.kg
r0_moon = CartesianRepresentation([3.844e8, 0, 0] * u.meter)
v0_moon = CartesianRepresentation([-1022, -1022, 1022] * u.meter / u.s)

def g(r: CartesianRepresentation): 
    return -((G * m_earth) / r.norm()**3) * r

r = {
    0 * u.s: r0_moon,
}
v = {
    0 * u.s: v0_moon,
}
a = {
    0 * u.s: CartesianRepresentation([0, 0, 0] * u.meter / u.s**2),
}
f = {
    0: g(r0_moon) * m_moon,
}

t = 0 * u.second
delta = 10 * u.second
limit = (30 * u.day).to(u.second)
i = 0
print("Starting...")
while t < limit:
    f[t + delta] = g(r[t]) * m_moon
    a[t + delta] = f[t + delta] / m_moon
    v[t + delta] = v[t] + (a[t + delta] * delta)
    r[t + delta] = r[t] + (v[t + delta] * delta)
    print(f"Timestep: {t} - {t.to(u.day).value:.2f} days ({r[t + delta].x.value:.2f}, {r[t + delta].y.value:.2f}, {r[t + delta].z.value:.2f})", end="\r")
    
    i += 1
    t = t + delta

fig = plt.figure(figsize=(8, 8))
axes = fig.axes(projection = '3d')
t = np.linspace(0, 1, 1000, endpoint=True)
axes.plot3D(t, signal.square(2 * np * 5 * t))
