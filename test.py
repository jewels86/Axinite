from astropy.coordinates import CartesianRepresentation
import astropy.units as u
import axinite as ax
import numpy as np
import math
import json 

sun = ax.Body("sun",
    1.989e30 * u.kg,
    CartesianRepresentation([0, 0, 0] * u.m),
    CartesianRepresentation([0, 0, 0] * u.m/u.s)
)
earth = ax.Body("earth",
    5.972e24 * u.kg,
    CartesianRepresentation([1.471e11, 0, 0] * u.m),
    CartesianRepresentation([0, 0, 3.03e4] * u.m/u.s)
)
moon = ax.Body("moon",
    7.342e22 * u.kg,
    CartesianRepresentation([3.844e8 + earth.r[0 * u.s].x.value, 0, 0] * u.m),
    CartesianRepresentation([0, 1.095e3, 1.095e3] * u.m/u.s)
)

bodies = [earth, sun, moon]

t = 0 * u.s
delta = (4 * u.hour).to(u.s)
limit = (360 * u.day).to(u.s)

while t < limit:
    for i, body in enumerate(bodies):
        others = [x for j, x in enumerate(bodies) if j != i]
        F_net = CartesianRepresentation([0, 0, 0] * u.kg * u.m/u.s**2)
        for o in others: F_net += o.gravitational_force(o.r[t] - body.r[t])

        a = F_net / body.mass
        body.v[t + delta] = body.v[t] + delta * a
        body.r[t + delta] = body.r[t] + delta * body.v[t + delta]

    t += delta
    print("Timestep: ", t, end="\r")

with open("test.ax", "w") as f:
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