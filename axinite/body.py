from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi
import numpy as np
import axinite as ax

class Body:
    def __init__(self, name: str, mass: np.float64, limit: np.float64, delta: np.float64, position: np.ndarray = None, velocity: np.ndarray = None):
        """Initializes a new Body object.

        Args:
            mass (u.Quantity): Mass of the object in kilograms.
            position (CartesianRepresentation): The initial position of the object.
            velocity (CartesianRepresentation): The initial velocity of the object.
        """
        self.mass = mass
        "The mass of the object in kilograms."

        self.name = name
        "The name of the object."

        self._inner = np.zeros(1, dtype=ax.body_dtype(limit, delta))

        if position is not None: self._inner["r"][0] = position
        if velocity is not None: self._inner["v"][0] = velocity

        self._inner["n"] = name
        self._inner["m"] = mass

    def r(self, t: np.float64) -> np.ndarray:
        """Returns the position of the object at a specific time.

        Args:
            t (np.float64): The time to get the position at.

        Returns:
            np.ndarray: The position of the object at the time.
        """
        return self._inner["r"][int(t)]

    def v(self, t: np.float64) -> np.ndarray:
        """Returns the velocity of the object at a specific time.

        Args:
            t (np.float64): The time to get the velocity at.

        Returns:
            np.ndarray: The velocity of the object at the time.
        """
        return self._inner["v"][int(t)]