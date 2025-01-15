import axinite as ax
import numpy as np
from numba import jit

@jit
def angle_between(v1, v2):
    """Calculates the angle between two vectors in radians.

    Args:
        v1 (np.ndarray): The first vector.
        v2 (np.ndarray): The second vector.

    Returns:
        float: The angle between the two vectors in radians.
    """
    unit_v1 = ax.unit_vector_jit(v1)
    unit_v2 = ax.unit_vector_jit(v2)
    dot_product = np.dot(unit_v1, unit_v2)
    angle_rad = np.arccos(ax.clip_scalar(dot_product, -1.0, 1.0))
    return angle_rad

@jit
def angle_between_degrees(v1, v2):
    """Calculates the angle between two vectors in degrees.

    Args:
        v1 (np.ndarray): The first vector.
        v2 (np.ndarray): The second vector.

    Returns:
        float: The angle between the two vectors in degrees.
    """
    angle_rad = angle_between(v1, v2)
    angle_deg = np.degrees(angle_rad)
    return angle_deg