import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _momentum_at(n: np.float64, bodies: np.ndarray):
    momentums = np.zeros((len(bodies), 3))
    for i, body in enumerate(bodies):
        momentums[i] = body["m"] * body["v"][n]
    return momentums

def momentum_at(n: np.float64, bodies: list[ax.Body]):
    return _momentum_at(n, ax.get_inner_bodies(bodies))

@jit 
def _total_momentum_at(n: np.float64, bodies: np.ndarray):
    return np.sum(_momentum_at(n, bodies), axis=0)

def total_momentum_at(n: np.float64, bodies: list[ax.Body]):
    return _total_momentum_at(n, ax.get_inner_bodies(bodies))

@jit
def _momentum(bodies: np.ndarray):
    momentums = np.zeros((len(bodies), bodies[0]["r"].shape[0], 3))
    n = 0
    while n < 0:
        momentums[n] = _momentum_at(n, bodies)
        n += 1
    return momentums

def momentum(bodies: list[ax.Body]):
    return _momentum(ax.get_inner_bodies(bodies))

@jit
def _total_momentum(bodies: np.ndarray):
    return np.sum(_momentum(bodies), axis=0)