import json
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
import axinite as ax

def show(path):
    with open(path, "r") as f:
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
        axes.set_facecolor('black')
        axes.set_xlabel('X')
        axes.set_ylabel('Z')
        axes.set_zlabel('Y')
        axes.legend(facecolor='black', edgecolor='white', labelcolor='white')

        lines = []
        animations = []

        for name, body in data["bodies"].items():
            x_pos = [r[0] for r in body["r"]]
            y_pos = [r[2] for r in body["r"]]
            z_pos = [r[1] for r in body["r"]]

            line = axes.plot3D(x_pos, y_pos, z_pos, label=name)
            lines.append(line)

        plt.show()

def load(path):
    with open(path, "r") as f:
        data = json.load(f)

        delta = data["delta"] * u.s
        limit = data["limit"] * u.s
        t = 0 * u.s
        bodies = []
        
        for name, body in data["bodies"]:
            bodies.append(ax.Body(name,
                body["m"] * u.kg,
                ax.functions.to_vector(body["r"], u.m),
                ax.functions.to_vector(body["v"], u.m / u.s)
            ))
        
        

def create():
    