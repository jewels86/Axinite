import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
b = 0.5 * P * A * C

r0 = r_initial
v0 = CartesianRepresentation(math.cos(theta) * v_initial, math.sin(theta) * v_initial, 0 * u.meter / u.second)

F_grav = m * g
def F_drag(v: CartesianRepresentation): return -0.5 * C * P * A * ax.vector_magnitude(v) * v
v = CartesianRepresentation([0, -156.96, 0] * u.meter / u.second)
print(f"{C} | {P} | {A} | {b} | {F_grav} | {ax.vector_magnitude(v)} | {v / ax.vector_magnitude(v)} | {F_drag(v)}")

f = {}
a = {}
v = {
    0: v0
}
r = {
    0: r0
}

delta_t = 1 * u.second
t = delta_t
tv = t.value
dtv = delta_t.value

while True:
    f[tv] = F_grav + F_drag(v[tv - dtv])
    a[tv] = f[tv] / m
    v[tv] = a[tv] * (dtv * u.second) + v[tv - dtv]
    r[tv] = v[tv] * (dtv * u.second) + r[tv - dtv]

    print(f"Timestep: {t}", end="\r")
    if (r[tv].y <= 0): break
    t += delta_t
    tv += dtv

print(f"Calculated {len(r)} timesteps.")

fig = plt.figure()
ax = plt.axes(projection='3d')
x_positions = [r[time].x.value for time in r]
y_positions = [r[time].z.value for time in r]
z_positions = [r[time].y.value for time in r]

plt.xlabel('X Position (meters)')
plt.ylabel('Y Position (meters)')
plt.grid(True)
plt.title('Projectile Motion')

line, = ax.plot3D(x_positions[0], y_positions[0], z_positions[0], label='Trajectory')

def update(frame):
    x = x_positions[:frame]
    y = y_positions[:frame]
    z = z_positions[:frame]
    line.set_xdata(x)
    line.set_ydata(y)
    line.set_3d_properties(z)
    return line

ani = animation.FuncAnimation(fig, update, frames=len(x_positions), repeat=False)
plt.show()