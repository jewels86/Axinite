import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _momentum_at(n: np.float64, bodies: np.ndarray) -> np.ndarray:
    """
    Calculate the momentum of each body at a specific timestep.

    Args:
        n (np.float64): The specific timestep.
        bodies (np.ndarray): Array of body representations.

    Returns:
        np.ndarray: Array of momenta for each body at the specified timestep.
    """
    momentums = np.zeros((len(bodies), 3))
    for i, body in enumerate(bodies):
        momentums[i] = body["m"] * body["v"][n]
    return momentums

def momentum_at(n: np.float64, bodies: list[ax.Body]) -> np.ndarray:
    """
    Calculate the momentum of each body at a specific timestep.

    Args:
        n (np.float64): The specific timestep.
        bodies (list[ax.Body]): List of body objects.

    Returns:
        np.ndarray: Array of momenta for each body at the specified timestep.
    """
    return _momentum_at(n, ax.get_inner_bodies(bodies))

@jit 
def _total_momentum_at(n: np.float64, bodies: np.ndarray) -> np.ndarray:
    """
    Calculate the total momentum of all bodies at a specific timestep.

    Args:
        n (np.float64): The specific timestep.
        bodies (np.ndarray): Array of body representations.

    Returns:
        np.ndarray: Total momentum of all bodies at the specified timestep.
    """
    return np.sum(_momentum_at(n, bodies), axis=0)

def total_momentum_at(n: np.float64, bodies: list[ax.Body]) -> np.ndarray:
    """
    Calculate the total momentum of all bodies at a specific timestep.

    Args:
        n (np.float64): The specific timestep.
        bodies (list[ax.Body]): List of body objects.

    Returns:
        np.ndarray: Total momentum of all bodies at the specified timestep.
    """
    return _total_momentum_at(n, ax.get_inner_bodies(bodies))

@jit
def _momentum(bodies: np.ndarray) -> np.ndarray:
    """
    Calculate the momentum of each body at all timesteps.

    Args:
        bodies (np.ndarray): Array of body representations.

    Returns:
        np.ndarray: Array of momenta for each body at all timesteps.
    """
    momentums = np.zeros((len(bodies), bodies[0]["r"].shape[0], 3))
    n = 0
    while n < bodies[0]["r"].shape[0]:
        momentums[:, n] = _momentum_at(n, bodies)
        n += 1
    return momentums

def momentum(bodies: list[ax.Body]) -> np.ndarray:
    """
    Calculate the momentum of each body at all timesteps.

    Args:
        bodies (list[ax.Body]): List of body objects.

    Returns:
        np.ndarray: Array of momenta for each body at all timesteps.
    """
    return _momentum(ax.get_inner_bodies(bodies))

@jit
def _total_momentum(bodies: np.ndarray) -> np.ndarray:
    """
    Calculate the total momentum of all bodies at all timesteps.

    Args:
        bodies (np.ndarray): Array of body representations.

    Returns:
        np.ndarray: Total momentum of all bodies at all timesteps.
    """
    return np.sum(_momentum(bodies), axis=0)

def total_momentum(bodies: list[ax.Body]) -> np.ndarray:
    """
    Calculate the total momentum of all bodies at all timesteps.

    Args:
        bodies (list[ax.Body]): List of body objects.

    Returns:
        np.ndarray: Total momentum of all bodies at all timesteps.
    """
    return _total_momentum(ax.get_inner_bodies(bodies))