"""
The `axinite` module provides the core functionality for the Axinite celestial mechanics engine.

This module includes classes and functions for representing celestial bodies, performing numerical integration
using various methods, and loading simulation data.
"""

from axinite.body import Body
from axinite.functions import vector_magnitude_jit, unit_vector_jit, gravitational_force_jit, body_dtype, \
    get_inner_bodies, _body, create_outer_bodies, timestep, interpret_distance, interpret_mass, interpret_time, \
    timesteps, clip_scalar, G, state, time_to, mass_to, distance_to, round_limit, gravitational_forces, locate_body
import axinite.functions as functions
from axinite.load import load
from axinite.backends.euler import euler_backend, euler_nojit_backend
from axinite.backends.verlet import verlet_backend, verlet_nojit_backend
from axinite.backends.rk2 import rk2_backend, rk2_nojit_backend
from axinite.backends.rk3 import rk3_backend, rk3_nojit_backend
from axinite.backends.rk4 import rk4_backend, rk4_nojit_backend
import axinite.backends as backends
import axinite.analysis as analysis
import axinite.tools as tools
import axinite.utils as utils
import axinite.analysis as axana
import axinite.tools as axtools
import axinite.utils as axutils
import axinite as ax