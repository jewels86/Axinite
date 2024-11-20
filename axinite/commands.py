import json
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation
from itertools import cycle

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

        lines = []
        animations = []
        colors = cycle(['red', 'lime', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'purple'])

        for name, body in data["bodies"].items():
            x_pos = [r[0] for r in body["r"]]
            y_pos = [r[2] for r in body["r"]]
            z_pos = [r[1] for r in body["r"]]

            line = axes.plot3D(x_pos, y_pos, z_pos, label=name, color=next(colors))
            lines.append(line)

        axes.legend(facecolor='black', edgecolor='white', labelcolor='white')
        plt.show()

def load(path):
    with open(path, "r") as f:
        data = json.load(f)

        delta = ax.functions.interpret_time(data["delta"])
        limit = ax.functions.interpret_time(data["limit"])
        t = 0 * u.s
        bodies = []
        
        for name, body in data["bodies"].items():
            bodies.append(ax.Body(name,
                body["mass"] * u.kg,
                ax.functions.to_vector(body["r"], u.m),
                ax.functions.to_vector(body["v"], u.m / u.s)
            ))
        
        while t < limit:
            for i, body in enumerate(bodies):
                others = [x for j, x in enumerate(bodies) if j != i]
                F_net = CartesianRepresentation([0, 0, 0] * u.kg * u.m/u.s**2)
                for o in others: F_net += o.gravitational_force(body.r[t] - o.r[t], body.mass)

                a = F_net / body.mass
                body.v[t + delta] = body.v[t] + delta * a
                body.r[t + delta] = body.r[t] + delta * body.v[t + delta]
            print(f"Timestep:  ({((t / limit).value * 100):.2f}%)", t, end="\r")
            t += delta
        print(f"Finished with {t / delta} timesteps")

        with open(f"{data["name"]}.ax", "w") as f:
            data = {
                "delta": delta.value,
                "limit": limit.value,
                "bodies": {}
            }
            for body in bodies:
                data["bodies"][body.name] = {
                    "mass": body.mass.value,
                    "r": [[r.x.value, r.y.value, r.z.value] for r in body.r.values()],
                }
            json.dump(data, f)