import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _collision_detection(bodies: np.ndarray, radii: np.ndarray):
    collisions = []
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            distance = np.linalg.norm(bodies[i]["r"] - bodies[j]["r"])
            if distance < (radii[i] + radii[j]):
                collisions.append((i, j))
    return collisions

def collision_detection(bodies: list[ax.Body], radii: np.ndarray, delta: np.float64):
    return _collision_detection(ax.get_inner_bodies(bodies), radii, delta)
