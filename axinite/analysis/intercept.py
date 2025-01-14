import axinite.tools as axtools
import numpy as np
from numba import njit

"""
A is intercepted
B is intercepting

Steps
1. Define inital values
    A. A's positions
    B. B's speed range
    C. Accuracy Parameter (number of speeds to check)
2. For each timestep
    A. Determine B's max-min distances and all in between
    B. Check if of A's position at that timestep matches up with any speeds
    C. If so, found
    D. Keep going other wise
"""

def intercept(a: axtools.Body, b: axtools.Body, speed_range: tuple[np.float64, np.float64], n_timesteps, k):
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
        speed_range, n_timesteps, k
    )

@njit
def _intercept(a, b, speed_range, n, k):
    speed_delta = (speed_range[1] - speed_range[0]) / k
    speeds = np.array([speed_range[0] + (speed_delta * i) for i in range(k)])

    for i in range(n):
        pos = a["r"][i]
        