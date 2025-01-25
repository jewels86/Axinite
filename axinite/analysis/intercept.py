import axinite.tools as axtools
import axinite as ax
import numpy as np
from numba import njit

def intercept(a: axtools.Body, b: axtools.Body, speed_range: tuple[np.float64, np.float64], n_timesteps, delta, verbose=False):
    """
    Attempt to intercept body 'a' with body 'b' within a given speed range and time steps.

    Args:
        a (axtools.Body): The intercepting body.
        b (axtools.Body): The target body.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.
        n_timesteps (int): The number of time steps to consider.
        delta (float): The time step interval.
        verbose (bool): Whether to print verbose output.

    Returns:
        tuple or None: Interception details (speed, position, timestep, unit vector) if found, otherwise None.
    """
    if verbose: print(f"Attempting to intercept {a.name} with {b.name}")
    dtype = np.dtype([
        ("n", "U20"),
        ("m", np.float64),
        ("r", np.float64, (n_timesteps, 3)),
        ("v", np.float64, (n_timesteps, 3)),
        ("rad", np.float64)
    ])
    return _intercept(
        np.array((a.name, a.mass, a._inner["r"], a._inner["v"], a.radius), dtype=dtype),
        np.array((b.name, b.mass, b._inner["r"], b._inner["v"], b.radius), dtype=dtype),
        speed_range, delta, n_timesteps, verbose
    )

@njit
def _intercept(a, b, speed_range, delta, n, verbose):
    """
    Numba-compiled function to attempt to intercept body 'a' with body 'b' within a given speed range and time steps.

    Args:
        a (np.ndarray): The intercepting body.
        b (np.ndarray): The target body.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.
        delta (float): The time step interval.
        n (int): The number of time steps to consider.
        verbose (bool): Whether to print verbose output.

    Returns:
        tuple or None: Interception details (speed, position, timestep, unit vector) if found, otherwise None.
    """
    _n = float(n)
    for i, r in enumerate(a["r"]):
        if verbose: print(f"Checking timestep {i} ({int(i/_n*100)}%)")
        unit_vector = ax.unit_vector_jit(r - b["r"][0])
        magnitude = ax.vector_magnitude_jit(r - b["r"][0])
        speed = magnitude / ((i + 1) * delta)
        if verbose: print(f"Speed: {int(speed)}\033[F\033[F")
        if speed_range[0] <= speed <= speed_range[1]: 
            print(f"\n\nFound!")
            return (speed, r, i, unit_vector)
    print("\n\nNot found")

    return None

def intercept_at(n, a, b, delta, speed_range):
    """
    Attempt to intercept body 'a' with body 'b' at a specific timestep.

    Args:
        n (int): The specific timestep to consider.
        a (axtools.Body): The intercepting body.
        b (axtools.Body): The target body.
        delta (float): The time step interval.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.

    Returns:
        tuple or None: Interception details (speed, position, timestep, unit vector) if found, otherwise None.
    """
    return _intercept_at(n, a._inner, b._inner, delta, speed_range)

@njit
def _intercept_at(n, a, b, delta, speed_range):
    """
    Numba-compiled function to attempt to intercept body 'a' with body 'b' at a specific timestep.

    Args:
        n (int): The specific timestep to consider.
        a (np.ndarray): The intercepting body.
        b (np.ndarray): The target body.
        delta (float): The time step interval.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.

    Returns:
        tuple or None: Interception details (speed, position, timestep, unit vector) if found, otherwise None.
    """
    unit_vector = ax.unit_vector_jit(b["r"][0] - a["r"][n])
    magnitude = ax.vector_magnitude_jit(b["r"][0] - a["r"][n])
    speed = magnitude / ((n + 1) * delta)
    if speed_range[0] <= speed <= speed_range[1]:
        return (speed, a["r"][n], n, unit_vector)
    return None