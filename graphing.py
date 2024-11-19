import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import axinite as ax
import json

with open("test.ax", "r") as f:
    data = json.load(f)

    fig = plt.figure(figsize=(8, 8))
    axes = fig.add_subplot(111, projection='3d')
    lines = []
    animations = []
    for name, body in data["bodies"].items():
        x_pos = [r[0] for r in body["r"]]
        y_pos = [r[2] for r in body["r"]]
        z_pos = [r[1] for r in body["r"]]

        line = axes.plot3D(x_pos, y_pos, z_pos, label=name)
        lines.append(line)
        
        # Plot initial position
        axes.scatter(x_pos[0], y_pos[0], z_pos[0], color='green', marker='o')
        # Plot end position
        axes.scatter(x_pos[-1], y_pos[-1], z_pos[-1], color='red', marker='x')
    
    axes.legend()
    plt.show()