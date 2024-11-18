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
    0 * u.s: g(r0_moon) * m_moon,
}

t = 0 * u.second
delta = 10 * u.second
limit = (30 * u.day).to(u.second)
i = 0
print("Starting...")

if os.path.exists('./test.ax'):
    print("Loading from file...")
    with open('test.ax', 'r') as file:
        data = json.load(file)
        r = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter) for k, v in data['r'].items()}
        v = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s) for k, v in data['v'].items()}
        a = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s**2) for k, v in data['a'].items()}
        f = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s**2) for k, v in data['f'].items()}
else:
    while t < limit:
        f[t + delta] = g(r[t]) * m_moon
        a[t + delta] = f[t + delta] / m_moon
        v[t + delta] = v[t] + (a[t + delta] * delta)
        r[t + delta] = r[t] + (v[t + delta] * delta)
        print(f"Timestep: {t} - {t.to(u.day).value:.2f} days ({r[t + delta].x.value:.2f}, {r[t + delta].y.value:.2f}, {r[t + delta].z.value:.2f})", end="\r")
        
        i += 1
        t = t + delta

    with open('test.ax', 'w') as file:
        data = {
            'r': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in r.items()},
            'v': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in v.items()},
            'a': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in a.items()},
            'f': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in f.items()},
        }
        json.dump(data, file)

last_entry = list(r.items())[-1]
print(f"Last entry in r: Time = {last_entry[0]}, Position = ({last_entry[1].x.value}, {last_entry[1].y.value}, {last_entry[1].z.value})")

fig = plt.figure(figsize=(8, 8))
axes = fig.add_subplot(111)

x_positions = [r[time].x.value for time in r]
z_positions = [r[time].z.value for time in r]

line, = axes.plot(x_positions[0], z_positions[0], 'b', label="Moon")

def update(frame):
    x = x_positions[:frame]
    z = z_positions[:frame]
    line.set_xdata(x)
    line.set_ydata(z)
    return line

ani = animation.FuncAnimation(fig, update, frames=len(x_positions), repeat=False, interval=1)
plt.xlabel('X Position (meters)')
plt.ylabel('Z Position (meters)')
plt.legend()
plt.show()