import numpy as np
import matplotlib.pyplot as plt
import matplitlib.animation as animation
import axinite as ax
import json

with open("test.ax", "r") as f:
    data = json.load(f)

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    lines = []
    for name, body in data["bodies"].items():
        x_pos = [r[0] for r in body["r"]]
        y_pos = [r[1] for r in body["r"]]
        z_pos = [r[2] for r in body["r"]]

        line = axes.plot([], [], [], label=name)
        lines.append(line)