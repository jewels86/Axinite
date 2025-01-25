import axinite as ax
import axinite.analysis as axana
import numpy as np

def _collision_detection(bodies: np.ndarray, radii: np.ndarray, delta: np.float64):
    n_total = bodies[0]["r"].shape[0]
    limit = n_total * delta
    collisions = []
    body_dtype = ax.body_dtype(limit, delta)
    collision = np.dtype([
        ("t", np.float64),
        ("n_range", np.int64, np.int64),
        ("accuracy", np.float64),
        ("bodies", np.ndarray[body_dtype])
    ])

    
    