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
    _bodies = backend(delta, limit, ax.get_inner_bodies(bodies), action=action, modifier=modifier, t=t.value, action_frequency=action_frequency)
    __bodies = []
    for body in _bodies:
        _body = ax.Body(body["n"], body["m"], limit, delta)
        _body._inner = body
        __bodies.append(_body)
    return __bodies
