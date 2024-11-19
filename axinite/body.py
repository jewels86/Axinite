from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi

class Body:
    def __init__(self, name, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation):
        self.mass = mass
        self.r = { 0 * u.s: position}
        self.v = { 0 * u.s: velocity}
        self.name = name

    def gravitational_acceleration(self, r: CartesianRepresentation):
        return -((G * self.mass) / vector_magnitude(r)**3) * r
    
    def gravitational_force(self, r: CartesianRepresentation, m: u.Quantity):
        return m * self.gravitational_acceleration(r)