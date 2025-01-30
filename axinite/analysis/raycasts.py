import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _can_see(a, b, bodies, radii, ai, bi):
    unit_vector = ax.unit_vector_jit(b["r"] - a["r"])
    distance_ab = np.linalg.norm(b["r"] - a["r"])

    for i, body in enumerate(bodies):
        if i == ai or i == bi:
            continue

        vector_ac = body["r"] - a["r"]

        projection_length = np.dot(vector_ac, unit_vector)
        closest_point = a["r"] + projection_length * unit_vector

        if 0 < projection_length < distance_ab:
            distance_to_line = np.linalg.norm(body["r"] - closest_point)
            if distance_to_line < radii[i]:
                return False

    return True

def can_see(a, b, bodies, radii):
    ai = next(i for i, body in enumerate(bodies) if np.array_equal(body["r"], a["r"]))
    bi = next(i for i, body in enumerate(bodies) if np.array_equal(body["r"], b["r"]))
    return _can_see(a, b, bodies, radii, ai, bi)