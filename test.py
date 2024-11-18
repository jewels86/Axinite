import axinite as ax
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import astropy.units as u
from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from scipy import signal
import json
import os
from mpl_toolkits.mplot3d import Axes3D

m_earth = 5.972e24 * u.kg
r0_earth = CartesianRepresentation([0, 0, 0] * u.meter)
v0_earth = CartesianRepresentation([0, 0, 0] * u.meter / u.s)

m_moon = 7.342e22 * u.kg
r0_moon = CartesianRepresentation([4.055e8, 0, 0] * u.meter)
v0_moon = CartesianRepresentation([0, 4022, 4022] * u.meter / u.s)

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
	0 * u.s: CartesianRepresentation([0, 0, 0] * u.kg * (u.meter / u.s**2)),
}

t = 0 * u.second
delta = 60 * u.second
limit = (100 * u.day).to(u.second)
i = 0
print("Starting...")

if os.path.exists('./test.ax'):
    print("Loading from file...")
    with open('test.ax', 'r') as file:
        data = json.load(file)
        r = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter) for k, v in data['r'].items()}
        v = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s) for k, v in data['v'].items()}

else:
    while t < limit:
	    f[t + delta] = -G * (m_earth / ax.vector_magnitude(r[t])**3) * r[t]
        a[t + delta] = f[t + delta] / m_moon
        v[t + delta] = v[t] + (a[t + delta] * delta)
        r[t + delta] = r[t] + (v[t + delta] * delta)
        print(f"Timestep: {t} - {t.to(u.day).value:.2f} days ({r[t + delta].x.value:.2f}, {r[t + delta].y.value:.2f}, {r[t + delta].z.value:.2f})", end="\r")
        
        i += 1
        t = t + delta
        
    print(r[t])

    with open('test.ax', 'w') as file:
        data = {
            'r': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in r.items()},
            'v': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in v.items()},
        }
        json.dump(data, file)

fig = plt.figure(figsize=(12, 12))  # Increased figure size
axes = fig.add_subplot(111, projection='3d')

x_positions = [r[time].x.value for time in r]
y_positions = [r[time].y.value for time in r]
z_positions = [r[time].z.value for time in r]

r_earth_radius = 6.371e6 * u.meter

line, = axes.plot3D(x_positions, y_positions, z_positions, 'b', label="Moon")
earth_point, = axes.plot3D(
    [r0_earth.x.value, r0_earth.x.value + r_earth_radius.value],
    [r0_earth.y.value, r0_earth.y.value],
    [r0_earth.z.value, r0_earth.z.value],
    'ro', label="Earth"
)
axes.legend()

plt.style.use('dark_background')

plt.show()