from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi
from numpy import float64

class Body:
    def __init__(self, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation):
        self.mass = mass
        self.r = { float64(0): position}
        self.v = { float64(0): velocity}

    def gravitational_force(self, r: CartesianRepresentation, m: u.Quantity):
        return -G * ((self.mass * m) / vector_magnitude(r)**2) * unit_vector(r)