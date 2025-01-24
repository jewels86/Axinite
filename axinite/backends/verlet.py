import numpy as np
from numba import jit
import axinite as ax

def verlet_nojit_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    """A integration backend for the Verlet method without JIT.

    Args:
        delta (np.float64): The change in time between each step.
        limit (np.float64): The maximum time of the simulation.
        bodies (np.ndarray): An array of bodies.
        action (function, optional): A function to be called with frequency action_frequency. Defaults to None.
        modifier (function, optional): A function to be called at every timestep to modify the forces on the bodies. Defaults to None.
        t (float, optional): The initial starting time of the simulation. Defaults to -1.0.
        action_frequency (int, optional): The frequency at which to call the action. Defaults to 200.

    Returns:
        np.ndarray: The bodies after the simulation.
    """

    if t is None:
        t = 0.0
    if t > 0.0:
        raise Exception("Verlet method does not support non-zero initial time.")
    t = 0.0 + delta 
    n = 1

    for i, body in enumerate(bodies):
        f = np.zeros(3)
        for j, other in enumerate(bodies):
            if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][0] - other["r"][0])
        if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)
        body["r"][1] = body["r"][0] + body["v"][0] * delta + 0.5 * (f / body["m"]) * delta**2
        body["v"][1] = (body["r"][1] - body["r"][0]) / (2 * delta)
    
    n += 1
    t += delta

    while t < limit:
        for i, body in enumerate(bodies):
            f = np.zeros(3)
            for j, other in enumerate(bodies):
                if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][n-1] - other["r"][n-1])
            if modifier is not None: f = modifier(body, f, bodies=bodies, t=t, delta=delta, limit=limit, n=n)

            body["r"][n] = body["r"][n-1] * 2 - body["r"][n-2] + (f / body["m"]) * delta**2
            body["v"][n] = (body["r"][n] - body["r"][n-1]) / (2 * delta)
        if action is not None and n % action_frequency == 0: action(bodies, t, limit=limit, delta=delta, n=n)
        n += 1
        t += delta
    
    return bodies

def verlet_backend(delta, limit, bodies, action=None, modifier=None, t=0.0, action_frequency=200):
    """A integration backend for the Verlet method with JIT.

    Args:
        delta (np.float64): The change in time between each step.
        limit (np.float64): The maximum time of the simulation.
        bodies (np.ndarray): An array of bodies.
        action (function, optional): A function to be called with frequency action_frequency. Defaults to None.
        modifier (function, optional): A function to be called at every timestep to modify the forces on the bodies. Defaults to None.
        t (float, optional): The initial starting time of the simulation. Defaults to 0.0.
        action_frequency (int, optional): The frequency at which to call the action. Defaults to 200.

    Returns:
        np.ndarray: The bodies after the simulation.
    """

    compiled = jit(verlet_nojit_backend, nopython=False)
    return compiled(delta, limit, bodies, action=action, modifier=modifier, t=t, action_frequency=action_frequency)