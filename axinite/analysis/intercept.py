import axinite.tools as axtools
import axinite as ax
import numpy as np
from numba import njit

def intercept(a: axtools.Body, b: axtools.Body, speed_range: tuple[np.float64, np.float64], n_timesteps, delta, verbose=False, max_thrust=1.0, d0=0.0, epsilon=1e-3, num_r=10, num_theta=18, num_phi=36):
    """
    Attempt to intercept body 'a' with body 'b' within a given speed range and time steps.

    Args:
        a (axtools.Body): The intercepting body.
        b (axtools.Body): The target body.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.
        n_timesteps (int): The number of time steps to consider.
        delta (float): The time step interval.
        verbose (bool): Whether to print verbose output.
        max_thrust (float): The maximum thrust available to the intercepting body.
        d0 (float): The initial distance offset.
        epsilon (float): The proximity threshold for interception.
        num_r (int): The number of radial divisions for search.
        num_theta (int): The number of polar angle divisions for search.
        num_phi (int): The number of azimuthal angle divisions for search.

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
        speed_range, delta, n_timesteps, verbose, max_thrust, d0, epsilon, num_r, num_theta, num_phi
    )

@njit
def _intercept(a, b, speed_range, delta, n, verbose, max_thrust=1.0, d0=0.0, epsilon=1e-3, num_r=10, num_theta=18, num_phi=36):
    """
    Numba-compiled function to attempt to intercept body 'a' with body 'b' within a given speed range and time steps.

    Args:
        a (np.ndarray): The intercepting body.
        b (np.ndarray): The target body.
        speed_range (tuple[np.float64, np.float64]): The range of speeds to consider for interception.
        delta (float): The time step interval.
        n (int): The number of time steps to consider.
        verbose (bool): Whether to print verbose output.
        max_thrust (float): The maximum thrust available to the intercepting body.
        d0 (float): The initial distance offset.
        epsilon (float): The proximity threshold for interception.
        num_r (int): The number of radial divisions for search.
        num_theta (int): The number of polar angle divisions for search.
        num_phi (int): The number of azimuthal angle divisions for search.

    Returns:
        tuple or None: Interception details (speed, position, timestep, unit vector) if found, otherwise None.
    """
    # Catalogue all positions of 'a' at each interval
    a_positions = a["r"]
    b_start = b["r"][0]
    min_speed, max_speed = speed_range
    for i in range(n):
        a_pos = a_positions[i]
        t = i * delta
        # The max distance b can travel at this timestep
        max_dist = d0 + max_thrust * t
        for r in np.linspace(0, max_dist, num_r):
            for theta in np.linspace(0, np.pi, num_theta):  # polar angle
                for phi in np.linspace(0, 2 * np.pi, num_phi):  # azimuthal angle
                    x = b_start[0] + r * np.sin(theta) * np.cos(phi)
                    y = b_start[1] + r * np.sin(theta) * np.sin(phi)
                    z = b_start[2] + r * np.cos(theta)
                    b_pos = np.array([x, y, z])
                    # Check if b_pos is close to a's current position
                    if np.linalg.norm(b_pos - a_pos) < epsilon:
                        unit_vector = (a_pos - b_start) / np.linalg.norm(a_pos - b_start)
                        return (r / t if t > 0 else 0, a_pos, i, unit_vector)
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