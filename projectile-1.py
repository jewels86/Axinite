import matplotlib.pyplot as plt
import numpy as np

from astropy import units as u
from astropy.coordinates import CartesianRepresentation
import math
import sympy as sp

h = 1.5 * u.meter
v_inital = 800 * (u.meter / u.second)
theta = 45
g = 9.8 * u.meter / u.second**2

r0 = CartesianRepresentation(0 * u.meter, h, 0 * u.meter)
v0 = CartesianRepresentation(math.cos(theta) * v_inital, math.sin(theta) * v_inital, 0 * u.meter / u.second)
a = CartesianRepresentation(0 * u.meter / u.second**2, -g, 0 * u.meter / u.second**2)

rt = lambda t: CartesianRepresentation(
    v_inital * math.cos(theta) * t, 
    h + ((v_inital * math.sin(theta) * t) - (0.5 * g * t**2)),
    0 * u.meter
)

delta_t = 1 * u.second
t = delta_t
dt_val = delta_t.value

r = {
    0: rt(0 * u.second)
}

while True:
    r[t] = rt(t)
    if r[t].y <= 0: break
    t = t + delta_t
    print("Timestep: ", t, end="\r")

print(f"Calculated {len(r)} timesteps.")
print("Starting position: ", r[0])
print("Ending position: ", r[t])
# Extract x and y positions for plotting
x_positions = [r[time].x.value for time in r]
y_positions = [r[time].y.value for time in r]

plt.figure(figsize=(10, 5))
plt.plot(x_positions, y_positions, marker='o')
plt.title('Projectile Motion')
plt.xlabel('X Position (meters)')
plt.ylabel('Y Position (meters)')
plt.grid(True)
plt.show()