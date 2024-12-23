import json
import numpy as np
import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation

def _load_legacy(delta: u.Quantity, limit: u.Quantity, *bodies: ax.Body, t: u.Quantity = 0 * u.s, modifiers: list = [], action=lambda *args, **kwargs: None):
    while t < limit:
        for body in bodies: 
            others = [b for b in bodies if b != body]
            f = CartesianRepresentation([0, 0, 0] * u.kg * u.m/u.s**2)
            
            for other in others: f += other.gravitational_force(body.r[t.value] - other.r[t.value], body.mass)
            for modifier in modifiers: f += modifier(body, t, bodies=bodies, f=f)

            a = f / body.mass
            v = body.v[t.value] + delta * a
            r = body.r[t.value] + delta * v

            body.r[t.value + delta.value] = r
            body.v[t.value + delta.value] = v
        t += delta
        action(t, limit=limit, bodies=bodies, delta=delta, modifiers=modifiers)
        
    return bodies