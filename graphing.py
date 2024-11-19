import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import axinite as ax
import json

with open("test.ax", "r") as f:
    data = json.load(f)

    fig = plt.figure(figsize=(8, 8), facecolor='black')
    axes = fig.add_subplot(111, projection='3d')
    axes.set_facecolor('black')
    axes.xaxis.label.set_color('white')
    axes.yaxis.label.set_color('white')
    axes.zaxis.label.set_color('white')
    axes.tick_params(axis='x', colors='white')
    axes.tick_params(axis='y', colors='white')
    axes.tick_params(axis='z', colors='white')
    axes.grid(color='black')
    lines = []
    animations = []
    
    for name, body in data["bodies"].items():
        x_pos = [r[0] for r in body["r"]]
        y_pos = [r[2] for r in body["r"]]
        z_pos = [r[1] for r in body["r"]]

        line = axes.plot3D(x_pos, y_pos, z_pos, label=name, color='cyan')
        lines.append(line)

axes.set_facecolor('black')
axes.set_xlabel('X')
axes.set_ylabel('Z')
axes.set_zlabel('Y')

axes.legend(facecolor='black', edgecolor='white', labelcolor='white')
plt.show()