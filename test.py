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
    const.M_earth.to(u.kg), 
    CartesianRepresentation([0, 0, 0] * u.kilometer), 
    CartesianRepresentation([0, 0, 0] * u.kilometer / u.second),
    const.R_earth.to(u.kilometer)
)
B = ax.Body(
    "B",
    7.342e22 * u.kg,
    CartesianRepresentation([405500, 0, 0] * u.kilometer),
    CartesianRepresentation([100, 100, 0] * u.kilometer / u.second),
    1737.4 * u.kilometer
)

t = 0
delta_t = 10 * u.second
dt_val = 10

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
    for i in range(0, 2628000):
        aB[t + dt_val] = A.gravitational_force(B)
        rB[t + dt_val] = (rB[t]) + (vB[t] * delta_t) + (0.5 * aB[t] * delta_t**2)
        vB[t + dt_val] = vB[t] + ((0.5 * (aB[t] + aB[t + dt_val])) * delta_t)
        t += dt_val
        print(f"Timestep: {t} ({round(t / 26200)}%)", end="\r")
except KeyboardInterrupt as e:
    pass

print("\nReady.")

def update(num, x_vals, y_vals, z_vals, line):
    line.set_data(x_vals[:num], y_vals[:num])
    line.set_3d_properties(z_vals[:num])
    return line,

fig = plt.figure()
ax = plt.axes(projection='3d')
x_vals = [pos.x.value for pos in rB.values()]
y_vals = [pos.y.value for pos in rB.values()]
z_vals = [pos.z.value for pos in rB.values()]

line, = ax.plot3D(x_vals, y_vals, z_vals, 'gray')
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')

ani = animation.FuncAnimation(fig, update, frames=len(x_vals), fargs=(x_vals, y_vals, z_vals, line), interval=10, blit=False)
plt.show()