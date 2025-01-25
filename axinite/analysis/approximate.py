import axinite as ax
import numpy as np
from scipy.interpolate import CubicSpline, CubicHermiteSpline
from numba import jit

def _approximate(body: np.ndarray, t: np.float64, delta: np.float64, interpolation_method):
    """
    Approximate the position and velocity of a body at a given time using a specified interpolation method.

    Args:
        body (np.ndarray): The inner representation of the body.
        t (np.float64): The time at which to approximate the position and velocity.
        delta (np.float64): The time step interval.
        interpolation_method (function): The interpolation method to use.

    Returns:
        np.ndarray: The approximated position and velocity of the body at time t.
    """
    n1 = np.floor(t / delta)
    n2 = np.ceil(t / delta)
    r1 = body["r"][n1]
    r2 = body["r"][n2]
    v1 = body["v"][n1]
    v2 = body["v"][n2]
    return interpolation_method(r1, r2, v1, v2, n1 * delta, n2 * delta, t)

def approximate(body: ax.Body, t: np.float64, delta: np.float64, interpolation_method: 'function'):
    """
    Approximate the position and velocity of a body at a given time using a specified interpolation method.

    Args:
        body (ax.Body): The body object.
        t (np.float64): The time at which to approximate the position and velocity.
        delta (np.float64): The time step interval.
        interpolation_method (function): The interpolation method to use.

    Returns:
        np.ndarray: The approximated position and velocity of the body at time t.
    """
    return _approximate(body._inner, t, delta, interpolation_method)

def _approximate_jit(body: np.ndarray, t: np.float64, delta: np.float64, interpolation_method):
    compiled = jit(_approximate)
    return compiled(body, t, delta, interpolation_method)

def approximate_jit(body: ax.Body, t: np.float64, delta: np.float64, interpolation_method: 'function'):
    """
    Approximate the position and velocity of a body at a given time using a specified interpolation method.

    Args:
        body (ax.Body): The body object.
        t (np.float64): The time at which to approximate the position and velocity.
        delta (np.float64): The time step interval.
        interpolation_method (function): The interpolation method to use.

    Returns:
        np.ndarray: The approximated position and velocity of the body at time t.
    """
    return _approximate_jit(body._inner, t, delta, interpolation_method)

@jit
def linear_interpolation(r1, r2, t1, t2, t):
    """
    Perform linear interpolation between two points.

    Args:
        r1 (np.ndarray): The position at the first time point.
        r2 (np.ndarray): The position at the second time point.
        t1 (np.float64): The first time point.
        t2 (np.float64): The second time point.
        t (np.float64): The time at which to interpolate.

    Returns:
        np.ndarray: The interpolated position at time t.
    """
    return r1 + (r2 - r1) * ((t - t1) / (t2 - t1))

def cubic_spline_interpolation(r1, r2, t1, t2, t):
    """
    Perform cubic spline interpolation between two points.

    Args:
        r1 (np.ndarray): The position at the first time point.
        r2 (np.ndarray): The position at the second time point.
        t1 (np.float64): The first time point.
        t2 (np.float64): The second time point.
        t (np.float64): The time at which to interpolate.

    Returns:
        np.ndarray: The interpolated position at time t.
    """
    times = np.array([t1, t2])
    points = np.array([r1, r2])
    spline = CubicSpline(times, points, axis=0)
    return spline(t)

def hermite_interpolation(r1, r2, v1, v2, t1, t2, t):
    """
    Perform Hermite interpolation between two points using position and velocity.

    Args:
        r1 (np.ndarray): The position at the first time point.
        r2 (np.ndarray): The position at the second time point.
        v1 (np.ndarray): The velocity at the first time point.
        v2 (np.ndarray): The velocity at the second time point.
        t1 (np.float64): The first time point.
        t2 (np.float64): The second time point.
        t (np.float64): The time at which to interpolate.

    Returns:
        np.ndarray: The interpolated position at time t.
    """
    times = np.array([t1, t2])
    points = np.array([r1, r2])
    velocities = np.array([v1, v2])
    spline = CubicHermiteSpline(times, points, velocities, axis=0)
    return spline(t)