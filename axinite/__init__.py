"""
The `axinite` module provides the core functionality for the Axinite celestial mechanics engine.

This module includes classes and functions for representing celestial bodies, performing numerical integration
using various methods, and loading simulation data.

Classes:
    Body: A class that represents a body in the simulation.

Functions:
    vector_magnitude_jit(vec: np.ndarray) -> float: Calculates the magnitude of a vector.
    unit_vector_jit(vec: np.ndarray) -> np.ndarray: Calculates the unit vector of a vector.
    gravitational_force_jit(m1: np.float64, m2: np.float64, r: np.ndarray) -> np.ndarray: Calculates the gravitational force between two bodies.
    body_dtype(limit: np.float64, delta: np.float64) -> np.dtype: Returns the data type for a body.
    get_inner_bodies(bodies: list[Body]) -> tuple: Returns the inner representation of a list of bodies.
    _body(limit: np.float64, delta: np.float64, name: str, mass: np.float64) -> np.ndarray: Creates a new body.
    create_outer_bodies(bodies: np.ndarray, limit: np.float64, delta: np.float64) -> list[Body]: Creates outer body representations from inner bodies.
    timestep(t: np.float64, delta: np.float64) -> int: Calculates the current timestep.
    load(delta: np.float64, limit: np.float64, backend: function, *bodies, t=0.0, modifier=None, action=None, action_frequency=200) -> np.ndarray: Loads a simulation from a backend.
    euler_backend(delta: np.float64, limit: np.float64, bodies: np.ndarray, action=None, modifier=None, t=0.0, action_frequency=200) -> np.ndarray: A integration backend for the Euler method with JIT.
    euler_nojit_backend(delta: np.float64, limit: np.float64, bodies: np.ndarray, action=None, modifier=None, t=0.0, action_frequency=200) -> np.ndarray: A integration backend for the Euler method without JIT.
    verlet_backend(delta: np.float64, limit: np.float64, bodies: np.ndarray, action=None, modifier=None, t=0.0, action_frequency=200) -> np.ndarray: A integration backend for the Verlet method with JIT.
    verlet_nojit_backend(delta: np.float64, limit: np.float64, bodies: np.ndarray, action=None, modifier=None, t=0.0, action_frequency=200) -> np.ndarray: A integration backend for the Verlet method without JIT.
"""

from axinite.body import Body
from axinite.functions import vector_magnitude_jit, unit_vector_jit, gravitational_force_jit, body_dtype, \
    get_inner_bodies, _body, create_outer_bodies, timestep, interpret_distance, interpret_mass, interpret_time, \
    timesteps, clip_scalar, G, state
import axinite.functions as functions
from axinite.load import load
from axinite.backends.euler import euler_backend, euler_nojit_backend
from axinite.backends.verlet import verlet_backend, verlet_nojit_backend
import axinite.backends as backends
import axinite.analysis as analysis
import axinite.tools as tools
import axinite.utils as utils