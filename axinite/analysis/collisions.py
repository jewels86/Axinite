import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _collision_detection(bodies: np.ndarray, radii: np.ndarray, delta: np.float64) -> np.ndarray:
    """
    Detect collisions between bodies within a given time step interval.

    Args:
        bodies (np.ndarray): Array of body representations.
        radii (np.ndarray): Array of radii for each body.
        delta (np.float64): Time step interval.

    Returns:
        np.ndarray: Array of detected collisions.
    """
    collisions = []
    n = 0
    n_total = bodies["r"].shape[0]
    limit = n_total * delta
    body_dtype = ax.body_dtype(limit, delta)
    collision_dtype = np.dtype([
        ("t", np.float64),
        ("n", np.int64),
        ("r", np.float64, 3),
        ("a", body_dtype),
        ("b", body_dtype)
    ])

    for i in range(n_total):
        for j in range(i + 1, n_total):
            dist = np.linalg.norm(bodies["r"][i] - bodies["r"][j])
            if dist < (radii[i] + radii[j]):
                collision = np.zeros(1, dtype=collision_dtype)
                collision["t"] = delta
                collision["n"] = n
                collision["r"] = (bodies["r"][i] + bodies["r"][j]) / 2
                collision["a"] = bodies[i]
                collision["b"] = bodies[j]
                collisions.append(collision)
                n += 1
            else:
                for t in np.arange(0, delta, delta / 10):
                    r_i = axana.approximate_jit(bodies[i], t, delta, axana.linear_interpolation)
                    r_j = axana.approximate_jit(bodies[j], t, delta, axana.linear_interpolation)
                    dist = np.linalg.norm(r_i - r_j)
                    if dist < (radii[i] + radii[j]):
                        collision = np.zeros(1, dtype=collision_dtype)
                        collision["t"] = t
                        collision["n"] = n
                        collision["r"] = (r_i + r_j) / 2
                        collision["a"] = bodies[i]
                        collision["b"] = bodies[j]
                        collisions.append(collision)
                        n += 1
                        break

    return np.array(collisions, dtype=collision_dtype)

def collision_detection(bodies: list[ax.Body], radii: np.ndarray, delta: np.float64) -> np.ndarray:
    """
    Detect collisions between bodies within a given time step interval.

    Args:
        bodies (list[ax.Body]): List of body objects.
        radii (np.ndarray): Array of radii for each body.
        delta (np.float64): Time step interval.

    Returns:
        np.ndarray: Array of detected collisions.
    """
    return _collision_detection(ax.get_inner_bodies(bodies), radii, delta)
