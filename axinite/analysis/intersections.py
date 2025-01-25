import axinite as ax
import numpy as np
from numba import jit

@jit
def _intersections(a: np.ndarray, b: np.ndarray, tol=1e-9) -> np.ndarray:
    """
    Find intersections between two sets of points within a given tolerance.

    Args:
        a (np.ndarray): First set of points.
        b (np.ndarray): Second set of points.
        tol (float): Tolerance for intersection detection. Intersections are considered valid if the denominator
                     of the intersection formula is greater than this tolerance.

    Returns:
        np.ndarray: Array of intersection points.
    """
    intersections = []
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            denom = (a[i+1, 0] - a[i, 0]) * (b[j+1, 1] - b[j, 1]) - (a[i+1, 1] - a[i, 1]) * (b[j+1, 0] - b[j, 0])
            if abs(denom) < tol:
                continue
            ua = ((b[j, 0] - a[i, 0]) * (b[j+1, 1] - b[j, 1]) - (b[j, 1] - a[i, 1]) * (b[j+1, 0] - b[j, 0])) / denom
            ub = ((b[j, 0] - a[i, 0]) * (a[i+1, 1] - a[i, 1]) - (b[j, 1] - a[i, 1]) * (a[i+1, 0] - a[i, 0])) / denom
            if 0 <= ua <= 1 and 0 <= ub <= 1:
                x = a[i, 0] + ua * (a[i+1, 0] - a[i, 0])
                y = a[i, 1] + ua * (a[i+1, 1] - a[i, 1])
                intersections.append((x, y))
    return np.array(intersections)

def intersections(a: ax.Body, b: ax.Body, tol=1e-9) -> np.ndarray:
    """
    Find intersections between two bodies within a given tolerance.

    Args:
        a (ax.Body): First body.
        b (ax.Body): Second body.
        tol (float): Tolerance for intersection detection. Intersections are considered valid if the denominator
                     of the intersection formula is greater than this tolerance.

    Returns:
        np.ndarray: Array of intersection points.
    """
    return _intersections(a._inner, b._inner, tol=tol)