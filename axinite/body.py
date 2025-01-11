from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi
import numpy as np

class Body:
    def __init__(self, mass: np.float64):
        """Initializes a new Body object.

        Args:
            mass (u.Quantity): Mass of the object in kilograms.
            position (CartesianRepresentation): The initial position of the object.
            velocity (CartesianRepresentation): The initial velocity of the object.
        """
        self.mass = mass
        "The mass of the object in kilograms."

        self.name = None
        "The name of the object."