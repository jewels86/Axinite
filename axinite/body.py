from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi

class Body:
    def __init__(self, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation):
        self.mass = mass
        self.r0 = position
        self.v0 = velocity

    def gravitational_acceleration(self, r: CartesianRepresentation):
        return -((G * self.mass) / vector_magnitude(r)**r) * unit_vector(r)
    
    def gravitational_force(self, r: CartesianRepresentation):
        return self.mass * self.gravitational_acceleration(r)