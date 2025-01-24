import axinite as ax
import numpy as np
from scipy.interpolate import CubicSpline, CubicHermiteSpline
from numba import jit

@jit
def _approximate(body: np.ndarray, t: np.float64, delta: np.float64, interpolation_method):
    n1 = np.floor(t / delta)
    n2 = np.ceil(t / delta)
    r1 = body["r"][n1]
    r2 = body["r"][n2]
    v1 = body["v"][n1]
    v2 = body["v"][n2]
    return interpolation_method(r1, r2, v1, v2, n1 * delta, n2 * delta, t)

def approximate(body: ax.Body, t: np.float64, delta: np.float64, interpolation_method: 'function'):
    return _approximate(body._inner, t, delta, interpolation_method)

def linear_interpolation(r1, r2, t1, t2, t):
    return r1 + (r2 - r1) * ((t - t1) / (t2 - t1))

def cubic_spline_interpolation(r1, r2, t1, t2, t):
    times = np.array([t1, t2])
    points = np.array([r1, r2])
    spline = CubicSpline(times, points, axis=0)
    return spline(t)

def hermite_interpolation(r1, r2, v1, v2, t1, t2, t):
    times = np.array([t1, t2])
    points = np.array([r1, r2])
    velocities = np.array([v1, v2])
    spline = CubicHermiteSpline(times, points, velocities, axis=0)
    return spline(t)