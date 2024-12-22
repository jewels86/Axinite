import numpy as np
import astropy.units as u
from astropy.constants import G
from astropy.coordinates import CartesianRepresentation
from numba import jit
import axinite as ax

def load_jit(delta: u.Quantity, limit: u.Quantity, action, *bodies: ax.Body, t: u.Quantity = 0 * u.s):
    @jit
    def compute_one_component(f: np.float64, mass: np.float64, prev_r: np.float64, prev_v: np.float64, _delta: np.float64):
        a = f / mass
        v = prev_v + _delta * a
        r = prev_r + _delta * v
        return r, v
    @jit
    def compute_gravity(m1, m2, r_mag, g=G.value):
        return g * (m1 * m2) / r_mag**2


    while t < limit:
        for body in bodies:
            others = [b for b in bodies if b != body]
            f = CartesianRepresentation([0, 0, 0] * u.kg * u.m/u.s**2)

            #print(body.r.keys(), t)

            for other in others:
                f = compute_gravity(body.mass.value, other.mass.value, ax.vector_magnitude(body.r[t.value] - other.r[t.value])) * ax.unit_vector(body.r[t.value] - other.r[t.value])
                rx, vx = compute_one_component(f.x.value, body.mass.value, body.r[t.value].x.value, body.v[t.value].x.value, delta.value)
                ry, vy = compute_one_component(f.y.value, body.mass.value, body.r[t.value].y.value, body.v[t.value].y.value, delta.value)
                rz, vz = compute_one_component(f.z.value, body.mass.value, body.r[t.value].z.value, body.v[t.value].z.value, delta.value)
                body.r[t.value + delta.value] = CartesianRepresentation([rx, ry, rz] * u.m)
                body.v[t.value + delta.value] = CartesianRepresentation([vx, vy, vz] * u.m/u.s)
        t += delta
        action(t, limit=limit, bodies=bodies)
        
    return bodies