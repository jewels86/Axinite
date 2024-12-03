import json
import numpy as np
import astropy.units as u
import axinite as ax
import astropy.units as u

def load(delta: u.Quantity, limit: u.Quantity, action, *bodies: ax.Body, t:u.Quantity=0):
    while t < limit:
        for body in bodies: 
            r, v = body.compute(t, delta, *[x for x in bodies if x != body])
            body.r[t.value + delta.value] = r
            body.v[t.value + delta.value] = v
        t += delta
        action(t, limit=limit, bodies=bodies)
        
    return bodies