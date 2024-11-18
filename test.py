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
r0_moon = CartesianRepresentation([3.63104e8, 0, 0] * u.meter)
v0_moon = CartesianRepresentation([0, 1022, 1022] * u.meter / u.s)

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
limit = (720 * u.day).to(u.second)
i = 0
print("Starting...")

section_size = (30 * u.day).to(u.second)  # Define the size of each section
section_count = 0

def save_section_data(r_section, v_section, section_count):
    data = {
        'r': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in r_section.items()},
        'v': {str(k.value): [v.x.value, v.y.value, v.z.value] for k, v in v_section.items()},
    }
    with open(f'test_section_{section_count}.ax', 'w') as file:
        json.dump(data, file)

if os.path.exists('./test.ax'):
    print("Loading from file...")
    with open('test.ax', 'r') as file:
        data = json.load(file)
        r = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter) for k, v in data['r'].items()}
        v = {u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s) for k, v in data['v'].items()}
else:
    while t < limit:
        r_section = {0 * u.s: r0_moon}
        v_section = {0 * u.s: v0_moon}
        while t < limit and t < (section_count + 1) * section_size:
            a_temp = -G * (m_earth / ax.vector_magnitude(r_section[t])**3) * r[t]
            v_temp = v_section[t] + (a_temp * delta)
            r_temp = r_section[t] + (v_temp * delta)
            r_section[t + delta] = r_temp
            v_section[t + delta] = v_temp
            print(f"Timestep: {t} - {t.to(u.day).value:.2f} days ({r_temp.x.value:.2f}, {r_temp.y.value:.2f}, {r_temp.z.value:.2f})", end="\r")
            
            i += 1
            t = t + delta
        
        save_section_data(r_section, v_section, section_count)
        section_count += 1
        tempr = r_section[t]
        tempv = v_section[t]
        r_section.clear()
        v_section.clear()
        r_section[t] = tempr
        v_section[t] = tempv

# Load all sections for plotting
r = {}
v = {}
for i in range(section_count):
    with open(f'test_section_{i}.ax', 'r') as file:
        data = json.load(file)
        r.update({u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter) for k, v in data['r'].items()})
        v.update({u.Quantity(float(k), u.s): CartesianRepresentation(np.array(v) * u.meter / u.s) for k, v in data['v'].items()})

fig = plt.figure(figsize=(12, 12))  # Increased figure size
axes = fig.add_subplot(111, projection='3d')

x_positions = [r[time].x.value for time in r]
y_positions = [r[time].y.value for time in r]
z_positions = [r[time].z.value for time in r]

r_earth_radius = 6.371e6 * u.meter

line, = axes.plot3D(x_positions, y_positions, z_positions, 'cyan', label="Moon")  # Bright color for the Moon
axes.scatter([r0_earth.x.value], [r0_earth.y.value], [r0_earth.z.value], color='yellow', s=100, label="Earth")  # Bright color for the Earth
axes.scatter([r0_moon.x.value], [r0_moon.y.value], [r0_moon.z.value], color='magenta', s=50, label="Initial Moon Position")  # Bright color for the initial Moon position
axes.legend()

axes.set_facecolor('black')
fig.patch.set_facecolor('black')

# Set bright colors for the grid and labels
axes.xaxis._axinfo['grid'].update(color = 'white')
axes.yaxis._axinfo['grid'].update(color = 'white')
axes.zaxis._axinfo['grid'].update(color = 'white')
axes.xaxis.label.set_color('white')
axes.yaxis.label.set_color('white')
axes.zaxis.label.set_color('white')
axes.tick_params(colors='white')

plt.show()