import axinite as ax
import numpy as np
from numba import jit

@jit
def _intersections(a: np.ndarray, b: np.ndarray, tol=1e-9):
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
    return intersections

def intersections(a: ax.Body, b: ax.Body, tol=1e-9):
	return _intersections(a._inner, b._inner, tol=tol)