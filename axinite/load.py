import axinite as ax
import numpy as np
import astropy.units as u
from astropy.coordinates import CartesianRepresentation
from numba import jit

def load(delta, limit, backend, *bodies, t=0 * u.s, modifier=None, action=None, action_frequency=200):
    """Loads a simulation from a backend.

    Args:
        delta (u.Quantity): The change in time between each step.
        limit (u.Quantity): The limit of the simulation.
        backend (function): The backend to load the simulation from.
        t (u.Quantity, optional): The initial time. Defaults to 0 * u.s.
        modifier (function, optional): The modifier to apply to forces in the simulation. Defaults to None.
        action (function, optional): An action to call with frequency `action_frequency`. Defaults to None.
        action_frequency (int, optional): The frequency at which to call the `action`. Defaults to 200.

    Returns:
        np.ndarray: An array of bodies.
    """
    body_dtype = np.dtype([
        ("m", np.float64),
        ("r", np.float64, (int(limit.value/delta.value), 3)),
        ("v", np.float64, (int(limit.value/delta.value), 3))
    ])
    _bodies = np.array([], dtype=body_dtype)
    for body in bodies:
        _r = body.r.values()
        _v = body.v.values()
        r = np.zeros((int(limit.value/delta.value), 3))
        v = np.zeros((int(limit.value/delta.value), 3))
        for i, __r in enumerate(_r): 
            r[i][0] = __r.x.value
            r[i][1] = __r.y.value
            r[i][2] = __r.z.value
        for i, __v in enumerate(_v):
            v[i][0] = __v.x.value
            v[i][1] = __v.y.value
            v[i][2] = __v.z.value
        _bodies = np.append(_bodies, np.array([
            (body.mass.value, r, v)
        ], dtype=body_dtype))
    _bodies = backend(delta.value, limit.value, _bodies, action=action, modifier=modifier, t=t.value, action_frequency=action_frequency)
    __bodies = ()
    for body in _bodies: 
        _body = ax.Body(body["m"] * u.kg, CartesianRepresentation(*body["r"][0], u.m), CartesianRepresentation(*body["v"][0], u.m/u.s))
        for i, r in enumerate(body["r"]):
            _body.r[i * delta.value] = CartesianRepresentation(*r, u.m)
        for i, v in enumerate(body["v"]):
            _body.v[i * delta.value] = CartesianRepresentation(*v, u.m/u.s)
        __bodies += (_body,)
    return __bodies
