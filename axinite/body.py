from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi
from numpy import float64

class Body:
    def __init__(self, name, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation, radius: u.Quantity):
        self.mass = mass
        self.r = { float64(0): position}
        self.v = { float64(0): velocity}
        self.name = name
        self.radius = radius

    def gravitational_acceleration(self, r: CartesianRepresentation):
        return -((G * self.mass) / vector_magnitude(r)**3) * r
    
    def gravitational_force(self, r: CartesianRepresentation, m: u.Quantity):
        return m * self.gravitational_acceleration(r)
    
    def compute(self, t, delta, *others: 'Body'):
        F_net = CartesianRepresentation([0, 0, 0] * u.kg * u.m/u.s**2)
        for body in others: F_net += body.gravitational_force(body.r[t.value] - self.r[t.value], self.mass)
        a = F_net / self.mass
        v = body.v[t.value] + delta * a
        r = body.r[t.value] + delta * v
        return r, v
        
        